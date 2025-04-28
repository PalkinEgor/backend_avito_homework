import requests

class PlateReaderClient:
    def __init__(self, host):
        self.host = host
    
    def read_image(self, image_id):
        url = f"{self.host}/images/{image_id}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Error while downloading image {response.status_code}")
        

if __name__ == '__main__':
    client = PlateReaderClient('http://89.169.157.72:8080')
    img = client.read_image(9965)
    print(img)