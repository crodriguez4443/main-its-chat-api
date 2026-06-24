import os
import glob
from bs4 import BeautifulSoup
import json
import csv
import re

import config


def generate_url(file_path, base_url=None):
    """Convert file path to proper URL based on content type patterns.

    base_url defaults to config.ARCHITECTURE_BASE_URL so each state
    deployment only needs to change the env var.
    """
    if base_url is None:
        base_url = config.ARCHITECTURE_BASE_URL
    filename = os.path.basename(file_path).replace('.htm', '')
    
    # Normalize path separators for comparison
    normalized_path = file_path.replace('\\', '/')

    #filter out the following content files
    remove_patterns =[  
        'interfaces.content.htm',
        'inventory.content.htm',
        'inventory.selector.htm',
        'invstake.content.htm',
        'invstake.selector.htm',
        'opsconstake.content.htm',
        'planobj.content.htm',
        'projects.content.htm',
        'projects.selector.htm',
        'projectselection.selector.htm',
        'projectsstake.content.htm',
        'projectsstake.selector.htm',
        'stakes.content.htm',
        'stakes.keywords.input.htm',
        'sakes.selector.htm',
        'servdesc.content',
        'servdesc.selector.htm',
        'services.selector.htm',
        'services.content.htm',
        'servstake.content.htm',
        'servstake.selector.htm',
        'planobj.htm'
        ]
    for pattern in remove_patterns:
        if filename == pattern:
            return None
    
    # Handle main directory files (not in content folder)
    if not normalized_path.startswith('../content/') and not 'content/' in normalized_path:
        return f"{base_url}/{filename}.htm"
    
    # Elemnt files: bundle52.htm -> bundle.htm?id=52
    if re.match(r'^bundle\d+$', filename):
        bundle_id = filename[6:]  # Remove 'bundle' prefix
        return f"{base_url}/bundle.htm?id={bundle_id}"

    # Element files: el599.htm -> element.htm?id=599
    if re.match(r'^el\d+$', filename):
        element_id = filename[2:]
        return f"{base_url}/element.htm?id={element_id}"
    
    # Functional requirements with element suffix: funreq_el970.htm -> funreq.htm?id=_el970
    elif re.match(r'^funreq_el\d+$', filename):
        element_id = filename[9:]  # Remove 'funreq_el' prefix
        return f"{base_url}/funreq.htm?id=_el{element_id}"
    
    # Regular functional requirements: funreq123.htm -> funreq.htm?id=123
    elif re.match(r'^funreq\d+$', filename):
        funreq_id = filename[6:]  # Remove 'funreq' prefix
        return f"{base_url}/funreq.htm?id={funreq_id}"
    
    # Plans: plan73.htm -> plandetail.htm?id=73
    elif re.match(r'^plan\d+$', filename):
        plan_id = filename[4:]  # Remove 'plan' prefix
        return f"{base_url}/plandetail.htm?id={plan_id}"
    
    # Flows: fl817.htm -> flow.htm?id=817
    elif re.match(r'^fl\d+$', filename):
        flow_id = filename[2:]  # Remove 'fl' prefix
        return f"{base_url}/flow.htm?id={flow_id}"
    
    # Interfaces: if44-937.htm -> interface.htm?id=44-937
    elif filename.startswith('if') and (filename[2:].replace('-', '').isdigit() or re.match(r'^if[\d-]+$', filename)):
        interface_id = filename[2:]  # Remove 'if' prefix
        return f"{base_url}/interface.htm?id={interface_id}"
    
    # Solutions: solution123.htm -> solution.htm?id=123
    elif re.match(r'^solution\d+$', filename):
        solution_id = filename[8:]  # Remove 'solution' prefix
        return f"{base_url}/solution.htm?id={solution_id}"
    
    # Projects: pr68.htm -> projdetail.htm?id=68
    elif re.match(r'^pr\d+$', filename):
        project_id = filename[2:]  # Remove 'pr' prefix
        return f"{base_url}/projdetail.htm?id={project_id}"
    
    # Stakeholders: stake123.htm -> stakeholder.htm?id=123
    elif re.match(r'^stake\d+$', filename):
        stake_id = filename[5:]  # Remove 'stake' prefix
        return f"{base_url}/stakeholder.htm?id={stake_id}"
    
    # For complex patterns like mpSH, TM, PT, CVO, etc. - use generic approach for now
    # These may need specific template pages or special handling
    else:
        # Default fallback - may need refinement for specific cases
        return f"{base_url}/spinstance.htm?id=/{filename}"

def clean_html_file(file_path):
    """Extract clean text from HTML file, removing nav/header/footer/scripts"""
    # Check if this file should be excluded
    generated_url = generate_url(file_path)
    if generated_url is None:
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Fall back to cp1252 for files with Windows-1252 encoded characters
        # (e.g., smart quotes like \x92, en-dashes \x96, non-breaking spaces \xa0)
        with open(file_path, 'r', encoding='cp1252') as f:
            content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Remove non-content elements
    for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
        element.decompose()

    # Get clean text
    clean_text = soup.get_text(strip=True, separator=' ')

    # Extract title from filename since these HTML fragments don't have title tags
    title = os.path.basename(file_path).replace('.htm', '')

    # File-type specific title extraction with proper elif chain
    if re.match(r'^el\d+\.htm$', os.path.basename(file_path)):
        element_name_cell = soup.find('td', string=lambda s: s and 'Element Name:' in s)
        if element_name_cell and element_name_cell.find_next_sibling('td'):
            title = element_name_cell.find_next_sibling('td').get_text(strip=True)
        else:
            # Fallback: try to find bold element name label
            label = soup.find('b', string=lambda s: s and "element name:" in s.lower())
            if label:
                sibling_td = label.find_parent('td').find_next_sibling('td')
                if sibling_td:
                    title = sibling_td.get_text(strip=True)

    elif re.match(r'^bundle\d+\.htm$', os.path.basename(file_path)):
        bundle_name_cell = soup.find('td', string=lambda s: s and 'Bundle Name:' in s)
        if bundle_name_cell and bundle_name_cell.find_next_sibling('td'):
            title = bundle_name_cell.find_next_sibling('td').get_text(strip=True)
        else:
            title = f"Bundle standard - {os.path.basename(file_path).replace('.htm', '').replace('bundle', '')}"

    elif re.match(r'^stake\d+\.htm$', os.path.basename(file_path)):
        stakeholder_name_cell = soup.find('td', string=lambda s: s and 'Stakeholder Name:' in s)
        if stakeholder_name_cell and stakeholder_name_cell.find_next_sibling('td'):
            title = stakeholder_name_cell.find_next_sibling('td').get_text(strip=True)
        else:
            title = f"Stakeholder {os.path.basename(file_path).replace('.htm', '').replace('stake', '')}"

    elif re.match(r'^plan\d+\.htm$', os.path.basename(file_path)):
        plan_name_cell = soup.find('td', string=lambda s: s and ("plan name:" in s.lower() or 'Strategy Name' in s))
        if plan_name_cell and plan_name_cell.find_next_sibling('td'):
            title = plan_name_cell.find_next_sibling('td').get_text(strip=True)
        else:
            title = f"Plan {os.path.basename(file_path).replace('.htm', '').replace('plan', '')}"

    elif re.match(r'^if[\d-]+\.htm$', os.path.basename(file_path)):
        interface_name_cell = soup.find('td', string=lambda s: s and 'Interface Name:' in s)
        if interface_name_cell and interface_name_cell.find_next_sibling('td'):
            title = interface_name_cell.find_next_sibling('td').get_text(strip=True)
        else:
            title = f"Interface {os.path.basename(file_path).replace('.htm', '').replace('if', '')}"

    elif re.match(r'^funreq(_el)?\d+\.htm$', os.path.basename(file_path)):
        table = soup.find('table')
        if table:
            funreq_name_cell = table.find('th')
            title = funreq_name_cell.get_text(strip=True)
        else:
            title = f"Function {os.path.basename(file_path).replace('.htm', '').replace('if', '')}"

    elif re.match(r'^fl\d+\.htm$', os.path.basename(file_path)):
        table = soup.find('table')
        if table:
            flow_name_row = table.find('td', string='Flow Name')
            title = flow_name_row.find_next_sibling('td').get_text(strip=True)  
        else:
            title = f"Flow {os.path.basename(file_path).replace('.htm', '').replace('if', '')}"  

    elif re.match(r'^pr\d+\.htm$', os.path.basename(file_path)):
        table = soup.find('table')
        if table:
            # Look for Project Name, Project Initiative Name, or Strategy Name
            project_cell = table.find(['strong', 'b'], string=lambda s: s and 
                ('Project Name:' in s or 'Project Initiative Name:' in s or 'Strategy Name' in s))
            if project_cell:
                title = project_cell.find_parent('td').find_next_sibling('td').get_text(strip=True)
            else:
                title = f"Project {os.path.basename(file_path).replace('.htm', '').replace('pr', '')}"

    else:
        title = f"Service Package {os.path.basename(file_path).replace('.htm', '')}"

    return {
        'url': generated_url,
        'source_file': file_path,
        'title': title,
        'content': clean_text,
        # 'word_count': len(clean_text.split())  <-- Removed to save space
    }

def process_all_content():
    """Process all HTML files in content directory"""
    content_data = []
    
    # Process files in content directory
    for file_path in glob.glob('../content/**/*.htm', recursive=True):
        try:
            data = clean_html_file(file_path)
            if data is not None:
                content_data.append(data)
                print(f"Processed: {file_path}")
            else:
                print(f"Skipped: {file_path} (excluded by filter)")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    # Also process main directory HTML files that contain content
    main_files = [
        '../index.htm', '../howto.htm', '../glossary.htm', '../conformance.htm',
        '../element.htm', '../stakeholder.htm', '../services.htm', '../projects.htm'
    ]

    for filename in main_files:
        if os.path.exists(filename):
            try:
                data = clean_html_file(filename)
                if data is not None:
                    content_data.append(data)
                    print(f"Processed: {filename}")
                else:
                    print(f"Skipped: {filename} (excluded by filter)")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    # Save processed content index
    with open('processed_content.json', 'w', encoding='utf-8') as f:
        json.dump(content_data, f, indent=2)
    
    print(f"Processed {len(content_data)} files")
    return content_data

def compress_content(content, max_length=9000):
    """Remove redundant phrases and conservatively truncate content"""
    # Define compression mappings
    replacements = [
        ("This standard (RFC)", "RFC"),
        ("This document specifies", "Specifies"),
        ("This document defines", "Defines"), 
        ("Simple Network Management Protocol (SNMP)", "SNMP"),
        ("Internet Protocol (IP)", "IP"),
        ("Management Information Base (MIB)", "MIB"),
        ("Dedicated Short Range Communication (DSRC)", "DSRC"),
        ("Road transport and traffic telematics", "RTTT"),
        ("Short Name DocNum FullName Description ", ""),
        ("Internet Control Message Protocol", "ICMP"),
        ("Transmission Control Protocol", "TCP"),
        ("User Datagram Protocol", "UDP"),
        ("IETF RFC ", "RFC "),
        ("Bundle: ", ""),
        # Additional aggressive compression
        (" defines ", " def "),
        (" specifies ", " spec "),
        (" standard ", " std "),
        (" protocol ", " proto "),
        (" implements ", " impl "),
        (" implementation ", " impl "),
        (" management ", " mgmt "),
        (" information ", " info "),
        (" communication ", " comm "),
        (" architecture ", " arch "),
        ("  ", " "),  # Remove double spaces
    ]
    
    compressed = content
    for old_phrase, new_phrase in replacements:
        compressed = compressed.replace(old_phrase, new_phrase)
    
    # Conservative truncation - keep first 9000 characters which contain most essential info
    if len(compressed) > max_length:
        # Find last complete sentence within limit
        truncated = compressed[:max_length]
        last_period = truncated.rfind('.')
        if last_period > max_length * 0.7:  # Only truncate at sentence if it's not too early
            compressed = truncated[:last_period + 1]
        else:
            compressed = truncated + "..."
    
    return compressed

def compress_title(title):
    """Remove redundant parts from titles"""
    # Remove "Bundle: " prefix and " - id:XXXX" suffix
    compressed = title.replace("Bundle: ", "")
    # Remove ID suffix pattern like " - id:1046"
    import re
    compressed = re.sub(r' - id:\d+$', '', compressed)
    return compressed

def compress_url(url):
    """Keep full URLs for better context"""
    return url

def json_to_csv(json_file="processed_content.json", csv_file="processed_content.csv"):
    """Convert processed_content.json to CSV format for LLM efficiency"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not data:
            print("No data found in JSON file")
            return
        
        # Write to CSV with reduced columns
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['url', 'title', 'content'])
            writer.writeheader()
            # Apply compression and write the fields we want
            for row in data:
                writer.writerow({
                    'url': compress_url(row['url']),
                    'title': compress_title(row['title']), 
                    'content': compress_content(row['content'])
                })
        
        # Compare file sizes
        json_size = os.path.getsize(json_file)
        csv_size = os.path.getsize(csv_file)
        compression_ratio = (1 - csv_size / json_size) * 100
        
        print(f"Converted {len(data)} entries to CSV")
        print(f"JSON size: {json_size:,} bytes")
        print(f"CSV size: {csv_size:,} bytes")
        print(f"Size reduction: {compression_ratio:.1f}%")
        
    except FileNotFoundError:
        print(f"File {json_file} not found")
    except Exception as e:
        print(f"Error converting to CSV: {e}")

def detect_content_type(url, title):
    """Detect content type based on URL patterns"""
    if '/bundle.htm?' in url:
        return 'bundle'
    elif '/element.htm?' in url or url.endswith('/element.htm'):
        return 'element'
    elif '/stakeholder.htm?' in url or url.endswith('/stakeholder.htm'):
        return 'stakeholder'
    elif '/funreq.htm?' in url:
        return 'funreq'
    elif '/plandetail.htm?' in url or '/plan' in url:
        return 'plan'
    elif '/flow.htm?' in url:
        return 'flow'
    elif '/interface.htm?' in url or url.endswith('/interface.htm'):
        return 'interface'
    elif '/projdetail.htm?' in url or url.endswith('/projects.htm'):
        return 'project'
    elif '/solution.htm?' in url:
        return 'solution'
    elif '/spinstance.htm?' in url:
        return 'service_package'
    else:
        return 'general'

def chunk_bundle_content(document, content):
    """Chunk bundle content by splitting on RFC boundaries"""
    chunks = []

    # Extract bundle ID from URL
    import re
    bundle_id_match = re.search(r'id=(\d+)', document['url'])
    parent_id = bundle_id_match.group(1) if bundle_id_match else 'unknown'

    # Split content by IETF RFC pattern
    rfc_pattern = r'(IETF RFC \d+)'
    parts = re.split(rfc_pattern, content)

    # Create bundle overview chunk (first part before any RFCs)
    if parts[0].strip():
        # Extract bundle name from the first part
        bundle_name_match = re.search(r'Bundle:\s*([^-]+)', parts[0])
        bundle_name = bundle_name_match.group(1).strip() if bundle_name_match else document['title']

        chunks.append({
            'url': document['url'],
            'title': f"{bundle_name} - Overview",
            'chunk_id': f"{parent_id}-0",
            'parent_id': parent_id,
            'chunk_type': 'bundle_header',
            'chunk_index': 0,
            'content': parts[0].strip()
        })

    # Process RFC chunks (parts come in pairs: "IETF RFC 123", "content")
    rfc_index = 1
    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            rfc_header = parts[i].strip()
            rfc_content = parts[i + 1].strip()

            # Extract RFC number
            rfc_num_match = re.search(r'RFC (\d+)', rfc_header)
            rfc_number = rfc_num_match.group(1) if rfc_num_match else str(rfc_index)

            # Combine header and content
            full_content = f"{rfc_header} {rfc_content}"

            # Extract RFC title (first occurrence after RFC number)
            title_match = re.search(r'RFC \d+\s+([^\n]+?)(?:\s+IETF RFC|\s+This standard|$)', full_content)
            rfc_title = title_match.group(1).strip() if title_match else f"RFC {rfc_number}"

            chunks.append({
                'url': document['url'],
                'title': f"{rfc_title}",
                'chunk_id': f"{parent_id}-{rfc_index}",
                'parent_id': parent_id,
                'chunk_type': 'rfc',
                'rfc_number': rfc_number,
                'chunk_index': rfc_index,
                'content': full_content
            })
            rfc_index += 1

    # Add total_chunks to all chunks
    for chunk in chunks:
        chunk['total_chunks'] = len(chunks)

    return chunks

def chunk_element_content(document, content):
    """Chunk element content - keep as single chunk with metadata"""
    # Extract element ID from URL
    import re
    element_id_match = re.search(r'id=(\d+)', document['url'])
    parent_id = element_id_match.group(1) if element_id_match else 'unknown'

    return [{
        'url': document['url'],
        'title': document['title'],
        'chunk_id': f"{parent_id}-0",
        'parent_id': parent_id,
        'chunk_type': 'element',
        'chunk_index': 0,
        'total_chunks': 1,
        'content': content
    }]

def chunk_stakeholder_content(document, content):
    """Chunk stakeholder content - keep as single chunk"""
    import re
    stake_id_match = re.search(r'id=(\d+)', document['url'])
    parent_id = stake_id_match.group(1) if stake_id_match else 'unknown'

    return [{
        'url': document['url'],
        'title': document['title'],
        'chunk_id': f"{parent_id}-0",
        'parent_id': parent_id,
        'chunk_type': 'stakeholder',
        'chunk_index': 0,
        'total_chunks': 1,
        'content': content
    }]

def chunk_generic_content(document, content, content_type):
    """Generic chunking for other content types - keep as single chunk"""
    import re
    # Try to extract ID from URL
    id_match = re.search(r'id=([^&]+)', document['url'])
    parent_id = id_match.group(1) if id_match else document['title'][:20]

    return [{
        'url': document['url'],
        'title': document['title'],
        'chunk_id': f"{parent_id}-0",
        'parent_id': str(parent_id),
        'chunk_type': content_type,
        'chunk_index': 0,
        'total_chunks': 1,
        'content': content
    }]

def chunk_content(document):
    """Main chunking function - routes to appropriate chunker based on content type"""
    content_type = detect_content_type(document['url'], document['title'])
    content = document['content']

    # Route to appropriate chunking function
    if content_type == 'bundle':
        return chunk_bundle_content(document, content)
    elif content_type == 'element':
        return chunk_element_content(document, content)
    elif content_type == 'stakeholder':
        return chunk_stakeholder_content(document, content)
    else:
        return chunk_generic_content(document, content, content_type)

def json_to_jsonl(json_file="processed_content.json", jsonl_file="processed_content.jsonl"):
    """Convert processed_content.json to JSONL format with intelligent chunking"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not data:
            print("No data found in JSON file")
            return

        all_chunks = []
        chunk_stats = {}

        # Process each document and chunk it
        for document in data:
            chunks = chunk_content(document)
            all_chunks.extend(chunks)

            # Track statistics
            content_type = detect_content_type(document['url'], document['title'])
            chunk_stats[content_type] = chunk_stats.get(content_type, 0) + len(chunks)

        # Write to JSONL (one JSON object per line)
        with open(jsonl_file, 'w', encoding='utf-8') as f:
            for chunk in all_chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + '\n')

        # Report statistics
        json_size = os.path.getsize(json_file)
        jsonl_size = os.path.getsize(jsonl_file)

        print(f"\n{'='*60}")
        print(f"JSONL Chunking Complete")
        print(f"{'='*60}")
        print(f"Original documents: {len(data)}")
        print(f"Total chunks created: {len(all_chunks)}")
        print(f"Average chunks per document: {len(all_chunks)/len(data):.1f}")
        print(f"\nChunks by content type:")
        for content_type, count in sorted(chunk_stats.items()):
            print(f"  {content_type}: {count} chunks")
        print(f"\nFile sizes:")
        print(f"  JSON: {json_size:,} bytes")
        print(f"  JSONL: {jsonl_size:,} bytes")
        print(f"  Size difference: {((jsonl_size - json_size) / json_size * 100):+.1f}%")
        print(f"\nOutput: {jsonl_file}")
        print(f"{'='*60}\n")

    except FileNotFoundError:
        print(f"File {json_file} not found. Please run process_all_content() first.")
    except Exception as e:
        print(f"Error converting to JSONL: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    process_all_content()
    json_to_csv()
    json_to_jsonl()