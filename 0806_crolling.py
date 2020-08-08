import requests
from bs4 import BeautifulSoup

url = 'https://movie.naver.com/movie/running/current.nhn#'
req = requests.get(url)

# 잘 받았나 확인해보기
# print(req)

soup = BeautifulSoup(req.text, 'html.parser')

#잘 받았는지 확인
# print(soup)

movie_list = soup.select(
    '#content > div.article > div.obj_section > div.lst_wrap > ul > li'
)
# 경로 확인
# print(movie_list)




final_movie_data = []


for li in movie_list:
    a_tag = li.select_one('dl.lst_dsc > dt > a')

    
    a_text = a_tag.get_text()
    a_href = a_tag['href']
    # 잘 나오나 확인
    # print(a_text)
    # print(a_href)
    code = a_href.split('=')[1]
    # print(code)

    movie_data ={
        'title' : a_text,
        'code' : code
    }

    final_movie_data.append(movie_data)


# print(final_movie_data)


for movie in final_movie_data:
    # 영화 리뷰는 헤더를 보지 않는다
    #=======================================
    # headers = {
    #     'authority': 'movie.naver.com',
    #     'upgrade-insecure-requests': '1',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #     'sec-fetch-site': 'same-origin',
    #     'sec-fetch-mode': 'navigate',
    #     'sec-fetch-dest': 'iframe',
    #     'referer': 'https://movie.naver.com/movie/bi/mi/point.nhn?code=189069',
    #     'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    #     'cookie': 'NNB=DGL42EFLEYBV6; nx_ssl=2; MM_NEW=1; NFS=2; MM_NOW_COACH=1; NRTK=ag#10s_gr#1_ma#-2_si#-2_en#-2_sp#-2; NM_THUMB_PROMOTION_BLOCK=Y; _ga=GA1.1.1242159289.1594274683; _ga_7VKFYR6RV1=GS1.1.1596563579.6.1.1596563842.60; NV_WETR_LOCATION_RGN_M="MDkxNDAxMDQ="; NV_WETR_LAST_ACCESS_RGN_M="MDkxNDAxMDQ="; JSESSIONID=7C68D2DCE92798208FB26750B89D719C; BMR=s=1596788559550&r=https%3A%2F%2Fm.blog.naver.com%2Fhoneywink529%2F221797975887&r2=; csrf_token=6737d3ca-6568-4cf9-b26c-b29530369de6',
    # }
    #========================================

    movie_code = movie['code']

    params = (
        ('code', movie_code),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )

    response = requests.get(
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', params=params)

    ifram_soup = BeautifulSoup(response.text, 'html.parser')

    review_list = ifram_soup.select(
        'body > div > div > div.score_result > ul > li'
    )

    count = 0

    for review in review_list:
        score = review.select_one('div.star_score > em').text
        reple = ''

        if review.select_one(f'div.score_reple > p > span#_filtered_ment_{count} > span#_unfold_ment{count}._unfold_ment') is None:
            reple = review.select_one(f'div.score_reple > p > span#_filtered_ment_{count}').text.strip()

        elif review.select_one(f'div.score_reple > p > span#_filtered_ment_{count} > span#_unfold_ment{count}'):
            reple = review.select_one(f'div.score_reple > p > span#_filtered_ment_{count} > span#_unfold_ment{count} > a')['data-src']
        
        print(score, reple)
        count += 1



