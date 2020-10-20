from textGoogleMatch import googleSearch,compareStr

copied_content="""HTML stands for Hyper Text Markup Language. HTML is the standard markup language for Web pages. HTML elements are the building blocks of HTML pages."""

data = googleSearch(copied_content)

for result in data:
    compare = compareStr(data[result]["description"],copied_content)
    if compare > 70:
        print(f'copied data form {data[result]["domain"]}')
