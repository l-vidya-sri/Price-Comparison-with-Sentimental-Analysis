import requests
from bs4 import BeautifulSoup

def get_price(url):
    # Send a GET request to the URL
    response = requests.get(url)

    description=''
    cnames=[]
    img=''
    prod_name=''
    prices=[]


    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'lxml')
        

        names = soup.find_all('div', class_='sm-content')
        for t in names:
            des = t.text.strip()
            print(des,'>>>>>') 
            description=des
            break


        
        names =soup.find_all('div', class_='pg-prd-head')
        print(names,'<<<<<<')
        for st in names:
            if st.find('h1'):
                n = st.find('h1').text
                print(n,'****')
                prod_name=n
                break



        img_tag = soup.find('div', class_='sm-swiper').find('img')
        if img_tag:
            image_source = img_tag['src']
            print(image_source,'________________')
            img=image_source
        else:
            print("Image source not found.")


    

        names =soup.find_all('div', class_='name')
        print(names,'<<<<<<')
        c=0

        for st in names:
            if st.find('span'): 

                company_name = st.find('span').text
                print(company_name,'****')
                cnames.append(company_name)
        print(cnames,'TTTTTTTTTTTTTTTTTTTTT')
            
        price_element = soup.find_all('span', class_='price')
        i=0
        for t in price_element:
            # Extract the price text
            price = t.text.strip()
            print(price)
            prices.append(price)
            if i>1:
                break
            i=i+1

        else:
            return 'Price not found on the page.'

    else:
        return f'Failed to retrieve the page. Status code: {response.status_code}'

    return prod_name, description, img, cnames, prices



if __name__ == '__main__':
    url = 'https://www.smartprix.com/mobiles/samsung-galaxy-s23-ultra-5g-ppd1q5mbifnl'
    price = get_price(url)
    print('----------------------------------------------------------------------------------------')
    print(price)
