from bs4 import BeautifulSoup
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def home():
    return {"message": "Welcome to the web scraping api!"}

class SpecsRequest(BaseModel):
    url: str

@app.post('/specs')
def specs(request: SpecsRequest):
    link = request.url
    if not link:
        raise HTTPException(status_code=400, detail="Missing 'url' parameter")

    response = requests.get(link)
    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to fetch page, status {response.status_code}"
        )

    soup = BeautifulSoup(response.text, 'html.parser')
    specs = [
        [spec.find('h3'), spec.find_all('li') or spec.find_all('p')]
        for spec in soup.find_all('div', class_='card-b -fh')
    ]
    final_specs = {}

    for spec in specs:
        if spec[0] is None:
            continue
        final_specs[spec[0].text] = [li.text for li in spec[1]]

    return final_specs