from bs4 import BeautifulSoup
from requests import get
import config, os

def clear_terminal():
    try :
        os.system('cls')
    except :
        os.system('clear')

def select_language():
    print(f"\n{config.RESET}[0] English-en\n[1] Arabic-ar\n[2] Russian-ru\n[3] Spanish-es\n[4] Japanese-ja\n[5] German-de\n[6] French-fr\n[7] Italian-it\n[8] Cheinese-zh\n[9] Persian-fa")
    language = int(input('\n\nPlease specify the language of search (use numbers) : '))
    
    if language not in list(range(10)):
        print(f'{config.RED} Invalid language choice choose one of the languages on the list :\n {config.RESET}')
        return select_language()

    return config.LANGUAGES[language]

def search_link(language):
    search_input = input(f'{config.GREEN}What to search for in {language}?: ')
    search_limit = input(f'{config.BLUE}How much results you want to apear (500 max)?: ')
    clear_terminal()
    
    return f"https://{language}.wikipedia.org/w/index.php?Search&limit={search_limit}&search={search_input}&fulltext=1&ns0=1" # &fulltext=1&ns0=1 is to make the page return search results and not direclty the most relevent search.

def search_results(search_link, language):
    results = []
    page = get(search_link, headers=config.HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    search_results = soup.find_all('li', class_='mw-search-result mw-search-result-ns-0')
    
    for result in search_results:
        heading = result.find('div', class_='mw-search-result-heading').find('a')
        title, link = heading.get('title'), heading.get('href')
        wiki_link = f"https://{language}.wikipedia.org" + link
        details = result.find('div', class_='searchresult').text
        additional_info = result.find('div', class_='mw-search-result-data').text
        
        results.append( { 'title': title, 'link': wiki_link, 'details': details, 'additional_info': additional_info } )
    
    return results

def pick_result(results):
    for index, result in enumerate(results) :
        print(f"{config.GREEN}----------------- [{index}] - {result['title']} -----------------")
        print(f"{config.CYAN}details: {result['details']}")
        print(f"{config.RESET}additional info: {result['additional_info']}\n\n")
        
    choice = int(input(f"{config.MAGENTA}Wich result you want? ( choose by index ): "))
    clear_terminal()
    
    return results[choice]['link']

def final_result(wiki_link):
    page = get(wiki_link, headers=config.HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    wiki = soup.find('div', class_='mw-content-ltr mw-parser-output').text
    
    return wiki

def wikifox():
    language = select_language()
    wiki_search_link = search_link(language)
    results = search_results(wiki_search_link, language)
    wiki_link = pick_result(results)
    result = final_result(wiki_link)
    print(result)
    
if __name__ == '__main__':
    wikifox()