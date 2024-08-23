import json
import requests
import csv


def main():
    # Read JSON data from a file
    try:
        with open('input_data.json', 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print("Error: input_data.json file not found.")
        return

    # API URL
    api_url = "https://api-sscasn.bkn.go.id/2024/portal/spf"

    # Headers
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://sscasn.bkn.go.id',
        'Referer': 'https://sscasn.bkn.go.id/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'sec-ch-ua': '^\\^"Not)A;Brand^\\^"',
        'Cookie': '8031e2dda37b1552a45b6fe38d7ed11d=94b11c704feea43266ed4a1b35555361; BIGipServerpool_prod_sscasn2024_kube=3104269322.47873.0000'
    }

    # Create CSV file
    with open('output.csv', 'w', newline='') as csvfile:
        fieldnames = ['cepat_kode', 'nama', 'tingkat_pendidikan_id', 'formasi_id', 'ins_nm', 'jp_nama', 'formasi_nm', 'jabatan_nm', 'lokasi_nm', 'jumlah_formasi', 'disable', 'gaji_min', 'gaji_max']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Iterate over each item in JSON data
        for item in data:
            cepat_kode = item['cepat_kode']
            nama = item['nama']
            tingkat_pendidikan_id = item['tingkat_pendidikan_id']

            # Initialize offset for pagination
            offset = 0
            total = 100  # Assuming a large total initially
            status = "in progress"

            # Print or log the status
            print(f"Data collection for {cepat_kode} is {status}")
            
            while offset < total:
                # Construct API URL with current offset
                api_params = {'kode_ref_pend': cepat_kode, 'offset': offset}
                response = requests.get(api_url, params=api_params, headers=headers)

                if response.status_code == 200:
                    try:
                        # Handle potential absence of "data" key
                        api_data = response.json()
                        total = api_data['data']['meta']['total']
                        for api_item in api_data['data']['data']:
                            api_item.update({'cepat_kode': cepat_kode, 'nama': nama, 'tingkat_pendidikan_id': tingkat_pendidikan_id})
                            writer.writerow(api_item)
                        offset += 10
                    except (KeyError, TypeError):
                        # Handle cases where "data" is missing or has unexpected structure
                        print(f"Warning: Unexpected response for {cepat_kode}: {response.text}")
                        total = 0  # Set total to 0 to stop further pagination

                else:
                    print(f"Error fetching data for {cepat_kode}: {response.text}")
                    break

            # Update status to "done" if all data has been collected
            if offset >= total:
                status = "done"

            # Print or log the status
            print(f"Data collection for {cepat_kode} is {status}")


if __name__ == "__main__":
    main()