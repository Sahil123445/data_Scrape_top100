import pandas as pd
import requests
from bs4 import BeautifulSoup

df = pd.DataFrame(columns=['Rank', 'Movie', 'Year', 'User Rating'])                                                         #An empty DataFrame with headers

imdb_urls = [
    'https://www.imdb.com/search/title/?groups=top_100&sort=user_rating,desc&view=simple',                                  #The IMDb URLs of the two search result pages
    'https://www.imdb.com/search/title/?groups=top_100&view=simple&sort=user_rating,desc&start=51&ref_=adv_nxt'
]

row_counter = 1                                                                                                             # Initialize a row counter

for i, url in enumerate(imdb_urls, start=1):                                                                                # Loop through the IMDb search result pages
    try:
        response = requests.get(url)                                                                                        # Send an HTTP GET request to the IMDb search result page

        if response.status_code == 200:                                                                                     # Check if the request was successful

            soup = BeautifulSoup(response.text, 'lxml')                                                                     # Parse the HTML content of the IMDb search result page using lxml

            movie_items = soup.select('.lister-item')                                                                       # Find all the movie items on the page

            for movie_item in movie_items:                                                                                  # Extract the movie titles, years, user ratings, and append them to the DataFrame
                movie_title_element = movie_item.select_one('.lister-item-header a')
                movie_year_element = movie_item.select_one('.lister-item-year')
                user_rating_element = movie_item.select_one('.col-imdb-rating strong')
                
                if movie_title_element:
                    movie_title = movie_title_element.get_text(strip=True)
                else:
                    movie_title = 'N/A'                                                                                     # If no movie title is found, set it to 'N/A'
                
                if movie_year_element:
                    movie_year = movie_year_element.get_text(strip=True).strip('()')
                else:
                    movie_year = 'N/A'                                                                                      # If no year is found, set it to 'N/A'
                
                if user_rating_element:
                    user_rating = user_rating_element.get_text(strip=True)
                else:
                    user_rating = 'N/A'                                                                                     # If no user rating is found, set it to 'N/A'
                
                df = pd.concat([df, pd.DataFrame({'Rank': [row_counter], 'Movie': [movie_title], 'Year': [movie_year], 'User Rating': [user_rating]})], ignore_index=True)
                row_counter += 1

            print(f'Successfully extracted data from Website {i}')                                                          # Print a message indicating success
        else:
            print(f'Failed to retrieve data from Website {i}')                                                              # Print an error message if the request was not successful

    except Exception as e:
        print(f'Error while processing Website {i}: {str(e)}')                                                              # Handle any exceptions that may occur during the process

df[['Rank', 'Movie', 'Year', 'User Rating']].to_csv('imdb_data.csv', index=False)                                           # Save the DataFrame as a CSV file in the same folder without the "Website" column

#print(df[['Rank', 'Movie', 'Year', 'User Rating']])                                                                        # Display the DataFrame

