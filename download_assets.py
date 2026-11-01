import urllib.request
import json
import os
import sys
import time

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) KannadaRajyotsava/1.0 (Educational; harishharsha819775@gmail.com)'

ENTRIES = {
    'actors': {
        'rajkumar': 'Dr._Rajkumar',
        'vishnuvardhan': 'Vishnuvardhan_(actor)',
        'ambareesh': 'Ambareesh',
        'shankar_nag': 'Shankar_Nag',
        'puneeth': 'Puneeth_Rajkumar',
        'saroja_devi': 'B._Saroja_Devi',
        'kalpana': 'Kalpana_(Kannada_actress)',
        'upendra': 'Upendra_(actor)',
        'sudeep': 'Sudeep',
        'yash': 'Yash_(actor)',
        'rishab_shetty': 'Rishab_Shetty',
    },
    'poets': {
        'pampa': 'Pampa_(poet)',
        'basavanna': 'Basava',
        'akka_mahadevi': 'Akka_Mahadevi',
        'purandara_dasa': 'Purandara_Dasa',
        'kanaka_dasa': 'Kanaka_Dasa',
        'kuvempu': 'Kuvempu',
        'bendre': 'D._R._Bendre',
        'karanth': 'K._Shivaram_Karanth',
        'masti': 'Masti_Venkatesha_Iyengar',
        'ananthamurthy': 'U._R._Ananthamurthy',
        'karnad': 'Girish_Karnad',
        'adiga': 'Gopalakrishna_Adiga',
        'gokak': 'V._K._Gokak',
    },
    'places': {
        'hampi': 'Hampi',
        'mysuru_palace': 'Mysore_Palace',
        'badami': 'Badami_cave_temples',
        'pattadakal': 'Pattadakal',
        'belur': 'Hoysaleswara_temple',
        'shravanabelagola': 'Gommateshwara_statue',
        'gol_gumbaz': 'Gol_Gumbaz',
        'jog_falls': 'Jog_Falls',
        'coorg': 'Kodagu_district',
        'gokarna': 'Gokarna,_India',
        'vidhana_soudha': 'Vidhana_Soudha',
        'nandi_hills': 'Nandi_Hills,_India',
        'dandeli': 'Dandeli',
    },
    'pride': {
        'formation': 'Karnataka_Rajyotsava',
        'districts': 'Districts_of_Karnataka',
        'bird': 'Indian_roller',
        'animal': 'Asian_elephant',
        'flower': 'Nelumbo_nucifera',
        'tree': 'Santalum_album',
        'history': 'Halmidi_inscription',
        'jnanpith': 'Jnanpith_Award',
    }
}

def fetch_and_download(category, key, title):
    os.makedirs(f'images/{category}', exist_ok=True)
    dest_path = f'images/{category}/{key}.jpg'
    
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        print(f'[*] Already exists: {dest_path}')
        return True

    time.sleep(1.5) # respectful delay to prevent 429

    
    # Check Wikipedia REST summary
    api_url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{title}'
    try:
        req = urllib.request.Request(api_url, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        
        img_url = None
        if 'thumbnail' in data and 'source' in data['thumbnail']:
            # Try to get higher res if possible by replacing thumbnail size
            src = data['thumbnail']['source']
            # standard thumb url: .../thumb/.../320px-... -> replace with 500px-...
            img_url = src
        elif 'originalimage' in data and 'source' in data['originalimage']:
            img_url = data['originalimage']['source']
            
        if not img_url:
            print(f'[-] No image found for {category}/{key} ({title})')
            return False
            
        # Download image
        img_req = urllib.request.Request(img_url, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(img_req, timeout=15) as img_resp:
            content = img_resp.read()
            with open(dest_path, 'wb') as f:
                f.write(content)
        print(f'[+] Downloaded {dest_path} ({len(content)} bytes)')
        return True
    except Exception as e:
        print(f'[!] Error fetching {category}/{key} ({title}): {e}')
        return False

def main():
    results = {}
    for cat, items in ENTRIES.items():
        for key, title in items.items():
            ok = fetch_and_download(cat, key, title)
            results[f'{cat}/{key}'] = ok
            
    print('\nSummary:')
    success = sum(1 for v in results.values() if v)
    total = len(results)
    print(f'Downloaded {success}/{total} images')

if __name__ == '__main__':
    main()
