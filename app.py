import crochet
crochet.setup()

from flask import Flask , render_template, jsonify, request, redirect, url_for
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
import time,os



from amazonScraper.amazonScraper.amazon_scraping import ReviewspiderSpider



app = Flask(__name__)

output_data = []
crawl_runner = CrawlerRunner()

@app.route('/')
def index():
	return render_template("index.html") 


@app.route('/', methods=['POST'])
def submit():
    if request.method == 'POST':
        s = request.form['url'] 
        global baseURL
        baseURL = s
        
        if os.path.exists("c:\\Users\\99450\\Desktop\\yusif\\tutorial\\outputfile.json"): 
        	os.remove("c:\\Users\\99450\\Desktop\\yusif\\tutorial\\outputfile.json")

        return redirect(url_for('scrape'))


@app.route("/scrape")
def scrape():
    global baseURL
    scrape_with_crochet(baseURL=baseURL) 
    time.sleep(20) 
    # for i in output_data:
    #     b = list(i.values())
    b = []
    a = list(output_data[0].keys())
    for i in output_data:
        b.append(list(i.values()))
    # return jsonify(output_data) # Returns the scraped data after being running for 20 seconds.
    return render_template('test.html', a=a, b=b)
  
  
@crochet.run_in_reactor
def scrape_with_crochet(baseURL):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    
    eventual = crawl_runner.crawl(ReviewspiderSpider, category = baseURL)
    return eventual

def _crawler_result(item, response, spider):
    output_data.append(dict(item))
    print(output_data)
    
    x = output_data[0]


if __name__== "__main__":
    app.run(debug=True)