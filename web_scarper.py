from bs4 import BeautifulSoup
import re
import json
import os
import sys

def web_scraper(html_path, html_element_name, elements_by = 'class', html_tag='span', cleand=False, many_elements=False, multi_line=False, numbered=False):
    """
    This is a function to scrape a hotel data from Booking.com

    Args:
      html_path: A string to specify the path to the HTML file extracted from Booking.com.
      html_element_name: A string to specify the class or id name of the text we want to extract, ex. (hp_hotel_name).
      elements_by: A string to specify the type of the HTML element ex. (class, id).
      html_tag: A string to specify the tag of the HTML element ex. (span, strong).
      cleand: A Boolean value to determine if we want to clean the text, the default value is False.
      many_elements: A Boolean value to determine if the desired text should be choose among more than one place, the default value is False.
      multi_line: A Boolean value to determine if the desired text contains mor than one line, the default value is False.
      numbered: A Boolean value to determine if the desired text contains mor than one line and needs to be numberd, the default value is False.

    Returns:
      A String of the hotel extracted information.
    """
    if os.path.isfile(html_path):
        if html_path.endswith('.html'):
            html_path = open(html_path).read()
            soup = BeautifulSoup(html_path, 'lxml')
            if many_elements:
                if multi_line:
                    hotel_info = """"""
                    if numbered:
                        num = 1
                        contents = soup.find_all(html_tag, {elements_by: html_element_name})
                        for content in contents:
                            string = content.text
                            string = re.sub('\n', '', string)
                            hotel_info = hotel_info + str(num) + '-' + string + '\n'
                            num +=1
                    else:
                        contents = soup.find(html_tag, {elements_by: html_element_name}).find_all('p')
                        for content in contents:
                            string = content.text
                            hotel_info = hotel_info + string + '\n'
                else:
                    hotel_info = soup.find_all(html_tag, {elements_by: html_element_name})[3].string
            else:
                hotel_info = soup.find(html_tag, {elements_by: html_element_name}).text
            if not cleand:
                hotel_info = re.sub('\n', '', hotel_info)
        else:
            print('THIS IS NOT HTML FILE!')
            print('Please select a path to HTML file, and try again')
            sys.exit(0)
    else:
        print('FILE NOT FOUND!')
        print('Please select a path to HTML file, and try again')
        sys.exit(0)

    return hotel_info

def save_to_json(output_path, file_name, dic_data):
    """
    This is a function to save the data to a JSON file

    Args:
      output_path: A string to specify the path where you want to save the JSON file.
      file_name: A string to specify the name of the file to be saved.
      dic_data: A Dictionary that contains the data that will be saved.

    Returns:
      A String JSON file .
    """
    json_path = os.path.join(output_path, file_name + '.json')
    with open(json_path, 'w') as outfile:
        json.dump(dic_data, outfile)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Wrong number of parameters. Please call this script with: python3 web_scarper.py <html_path> <output_path>")
        print("------>")
        print("For example: python3 web_scarper.py 'input/Kempinski Hotel Bristol Berlin, Germany - Booking.com.html' 'output'")
        sys.exit(0)
    html_path = sys.argv[1]
    output_path = sys.argv[2]
    print('STARTED')
    hotel_info = { }
    hotel_name = web_scraper(html_path, 'hp_hotel_name', 'id', 'span')
    hotel_info['Hotel_Name'] = hotel_name
    hotel_info['Hotel_Address'] = web_scraper(html_path, 'hp_address_subtitle', 'id', 'span')
    hotel_info['Hotel_Classification'] = web_scraper(html_path, 'invisible_spoken', 'class', 'span', True, True)
    hotel_info['Hotel_Review_points'] = float(web_scraper(html_path, 'average', 'class', 'span', True))
    hotel_info['Hotel_Number_of_reviews'] = int(web_scraper(html_path, 'count', 'class', 'strong', True))
    hotel_description_1 = web_scraper(html_path, 'summary', 'id', 'div', True, True, True, False)
    hotel_description_2 = web_scraper(html_path, 'hotel_meta_style', 'class', 'p', True, False, False, False)
    hotel_info['Hotel_Description'] = hotel_description_1 + hotel_description_2
    hotel_info['Hotel_room_Categories'] = web_scraper(html_path, 'ftd', 'class', 'td', True, True, True, True)
    hotel_info['Alternative_Hotels'] = web_scraper(html_path, 'althotel_link', 'class', 'a', True, True, True, True)

    save_to_json(output_path, hotel_name, hotel_info)
    
    print('completed successfully')