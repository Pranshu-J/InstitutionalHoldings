import requests

def process_next_url():
    """
    Reads the first line from 'urls.txt' (assumed to be a URL to a .txt file),
    fetches the content from that URL using provided headers, saves it as 'filing.txt',
    and then removes the first line from 'urls.txt' by shifting the remaining lines up.
    """
    # Read the first line from urls.txt
    try:
        with open('urls.txt', 'r') as f:
            first_line = f.readline().strip()
        if not first_line:
            print("urls.txt is empty.")
            return
    except FileNotFoundError:
        print("urls.txt not found.")
        return

    # Define headers to mimic browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Cookie': 'ak_bmsc=572034F5EDD328619CD8A1FCCC5ABA7D~000000000000000000000000000000~YAAQDupCFzAKz1aZAQAAiCL5fR1sVpBchCBnhChdd5WMrB14/cgKSBhJrfyE9RLRXOi6jIuU94kuqsovV+P5ygMJe0YwkwZxwUHGAvTI/xHeVvmVbRk4CkCV3kJXIgodt0nrFvxYsaKZrRPLFACmsAoGbeRZBBcosb3StWkGeLKe9QXHPMEUwZgdffXZexjPN4TCabAphgHmT3JaT4OA1ow0qGJWcfmDcvU2wGn3WbkMPIRsJIm5EF58B+pF6oP6XMbdQ2HWXZOUzYdIQaL3dKgeQvBpy4x5UlKz/69vo2leHkzo1iyJ5dCwKjr0jOTP//YV5okePjFsbEpHIB+t7hrAHob6rRjDV4MUNeaUDs10eCwJG032eVxiGvekPymdrrfrC3lzO9E=; bm_mi=4582225AF61C53FBA226CCB0F863C953~YAAQDupCF+Qkz1aZAQAAA076fR3+RYfLroNHmHcf3sQRM0EeTMZBDWcT640zSpJWzenDNRgWTSaiDuVSEswyxAJ23lUxYnCypEeN5l4BOvFGNBspjPovLVLcBq6zRmxl9xGHZo0TTLaNLwTNnZQanfVxBGcaNbqdGSpzBiojk6nuxOWhmMsTXlwnEhQ/UzykZaL9dgbF4i2q67Lp2Or33cinF0INnIs09lU7Iljj7k8AAfpAyMIWc1S/pPGVojlZElWF7FOvOpeWugx91l12336Jar6DDemwYKcZ/mzSWLI53bnyQN1b79rDykdb+30mFzYRp/b0qd9N9aRiMSM1~1; bm_sv=6DFED25A53EF41E1FE171145866D3D32~YAAQDupCF40mz1aZAQAAmmr6fR3Z5TxAkwQiT7WUV4/kXi8ERCBayBrTexdFVGHQZWDLq85p2Bbpk8SobbuK3uBgW0rNIxU/Gvrd3EnTUbtAIpncrdnKLfVk6bMxQWHyth7hFAMxbruFY4nTxRB7JtZYOJ259lXRcctkbnQY5EpuZcaiwDYX8gAijqxKzsojA5s72Ta1V0sI2a+fzv6hS0RYKgrk5+NjTjav5yL7iNsnu4AOt9Xi8yIe4nCo~1',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0, i'
    }

    # Fetch the content from the URL and save as filing.txt
    try:
        response = requests.get(first_line, headers=headers)
        if response.status_code == 200:
            with open('filing.txt', 'w') as f:
                f.write(response.text)
            print(f"Successfully saved content from {first_line} to filing.txt")
        else:
            print(f"Failed to fetch URL: {response.status_code} - {response.reason}")
            return
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return

    # Remove the first line from urls.txt by rewriting the file without it
    try:
        with open('urls.txt', 'r') as f:
            lines = f.readlines()
        with open('urls.txt', 'w') as f:
            for line in lines[1:]:
                f.write(line)
        print("First line removed from urls.txt")
    except Exception as e:
        print(f"Error updating urls.txt: {e}")