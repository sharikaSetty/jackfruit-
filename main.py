import requests, sys, json
from tabulate import tabulate
from pyfiglet import Figlet


def main():
    lat, long=get_area(input('Enter Area Name: '))
    weather(lat,long)



def get_area(ar):
    try:
        response=requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={ar}&appid={'0da102f5f62e49334448cfe39a3159a8'}')
        data=response.json()
        if not data:
            raise Exception()
    except Exception:
        sys.exit('invalid area name')
    return data[0]['lat'],data[0]['lon']



def weather(lat,long):
    try:
        response=requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={'e8cde7fb8c3391c297d032915416fe6c'}')
    except Exception as e:
        print('Error:',e)
    data=response.json()
    f_data={
        'Location':data['name'],
        'Country':data['sys']['country'],
        'Timezone':data['timezone'],
        'Temperature':data['main']['temp'],
        'Humidity':data['main']['humidity'],
        'Pressure':data['main']['pressure'],
        'Weather Description':data['weather'][0]['description'],
        'Wind Speed':data['wind']['speed']
    } 
    print(Figlet(font='slant').renderText('Weather Report'))
    print( tabulate(f_data.items(),headers=['PARAMETER','VALUE'],tablefmt='grid')) 
    #print(json.dumps(data, indent=4))
    

if __name__=='__main__':
    main()