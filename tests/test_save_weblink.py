import requests

def save_weblink(url, file_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        print(f"{response.headers=}")
        print(f"Response: {response}, MIME type: {response.headers.get('Content-Type')}")
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return True
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False


# save_weblink("https://huggingface.co/google/flan-t5-xxl", "tmp/t5.html")
# save_weblink("https://arxiv.org/pdf/2412.01253", "tmp/paper.pdf")

import wget
url = 'https://www.cs.ucr.edu/~cshelton/cppsem/simpmat.cc'

url = 'https://arxiv.org/pdf/2412.01253'

filename = wget.download(url, out="tmp", bar=lambda current_size, total_size, width: print(current_size, total_size, width))
print(filename)

response = requests.head(url)
print(response.headers)
print(response.headers.get('Content-Type'))