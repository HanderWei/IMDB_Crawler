import pymongo
from pymongo import MongoClient
import pygal
import operator
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

client = MongoClient('localhost', 27017)
db = client['imdb']
top250 = db['top250']
output_path = "chart/"

my_style = LS("#e3b038", base_style=LCS)

my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False


def get_countries_statistics():
    """统计TOP250各国电影数量"""
    # 找出所有出现过的国家
    countries = top250.distinct("country")
    countries_dict = {}
    for country in countries:
        # 计算该国出现在TOP250的电影数量
        countries_dict[country] = top250.find({"country": country}).count()
    sorted_dict = dict(sorted(countries_dict.items(), key=operator.itemgetter(1), reverse=True))
    return sorted_dict


def generate_countries_bar(countries, filename):
    """生成国家数量统计直方图"""
    bar = pygal.Bar(my_config, style=my_style)
    bar.title = "IMDB TOP250 Country Statistics"
    bar.y_title = "Movies Count"
    bar.x_labels = countries.keys()
    bar.add("", values=countries.values())
    bar.render_to_file(filename)


def generate_all_countries_bar():
    countries = get_countries_statistics()
    generate_countries_bar(countries, filename=(output_path + 'countries.svg'))


def generate_country_bar_without_usa():
    countries = get_countries_statistics()
    del countries['USA']
    generate_countries_bar(countries, filename=(output_path + 'contries_without_usa.svg'))


def get_year_statistics():
    """统计TOP250每年出现的电影数量"""
    # 找出最早的年份以及最新的年份
    years = top250.distinct("year")
    sorted_years = sorted(years)

    oldest = sorted_years[0]
    newest = sorted_years[-1]

    years_dict = {}
    for year in range(oldest, newest + 1):
        # 统计该年份出现在TOP250榜单的电影数量
        years_dict[year] = top250.find({"year": year}).count()
    return years_dict


def generate_years_line():
    """生成年份折线图"""
    years_statistics = get_year_statistics()
    line = pygal.Line(my_config, style=my_style, show_minor_x_labels=False)
    line.title = "IMDB TOP250 Year Statistics"
    line.y_title = "Movies Count"
    years = list(years_statistics.keys())
    line.x_labels = map(str, range(years[0], years[-1] + 1))
    line.x_labels_major = list(range(years[0], years[-1], 10))

    line.add("", values=years_statistics.values())
    line.render_to_file(output_path + "years.svg")


def get_generation_statistics():
    """统计每个年代在TOP250榜单上出现的电影数量"""
    start = 1920
    step = 10
    generation_dict = {}
    while start < 2011:
        count = 0

        for i in range(0, step):
            count = count + top250.find({"year": start + i}).count()
        generation_dict[str(start) + 's'] = count
        start = start + step
    return generation_dict


def generate_generation_bar():
    """生成每个年代电影数量直方图"""
    generations = get_generation_statistics()
    bar = pygal.Bar(my_config, style=my_style, x_label_rotation=0)
    bar.title = "IMDB TOP250 Generation Statistics"
    bar.y_title = "Movies Count"
    bar.x_labels = generations.keys()
    bar.add("", values=generations.values())
    bar.render_to_file(output_path + "generations.svg")


def get_all_genre():
    """获取全部类型"""
    all_genre = set()
    for movie in top250.find():
        for genre in movie['genre']:
            all_genre.add(genre)
    return all_genre


def get_genre_statistics():
    """统计每种类型片在TOP250的电影数量"""

    # 初始化
    genre_dict = {}
    all_genre = get_all_genre()
    for genre in all_genre:
        genre_dict[genre] = 0

    # 统计每部电影
    for movie in top250.find():
        for genre in movie['genre']:
            genre_dict[genre] = genre_dict[genre] + 1
    sorted_dict = dict(sorted(genre_dict.items(), key=operator.itemgetter(1), reverse=True))
    return sorted_dict


def generate_genre_bar():
    """生成类型统计直方图"""
    genres = get_genre_statistics()
    bar = pygal.Bar(my_config, style=my_style)
    bar.title = "IMDB TOP250 Genre Statistics"
    bar.y_title = "Movies Count"
    bar.x_labels = genres.keys()
    bar.add("", values=genres.values())
    bar.render_to_file(output_path + "genres.svg")


def rating_count_top_10():
    """统计评价人数最多的十部电影"""
    movies = top250.find().sort("ratingCount", pymongo.DESCENDING).limit(10)
    movies_dict = {}
    for movie in movies:
        movies_dict[movie['title']] = movie['ratingCount']
    return movies_dict


def generate_rating_count_top_10_bar():
    """生成类型统计直方图"""
    movies_dict = rating_count_top_10()
    bar = pygal.Bar(my_config, style=my_style)
    bar.title = "IMDB Rating Count TOP10 Statistics"
    bar.y_title = "Movies Count"
    bar.x_labels = movies_dict.keys()
    bar.add("", values=movies_dict.values())
    bar.render_to_file(output_path + "rating_count_top10.svg")


def get_all_directors():
    """获取全部导演"""
    all_directors = set()
    for movie in top250.find():
        for director in movie['director']:
            all_directors.add(director)
    return all_directors


def get_director_statistics():
    """统计每个导演在TOP250的电影数量"""

    # 初始化
    director_dict = {}
    all_director = get_all_directors()
    for director in all_director:
        director_dict[director] = 0

    # 统计每部电影
    for movie in top250.find():
        for director in movie['director']:
            director_dict[director] = director_dict[director] + 1
    sorted_dict = dict(sorted(director_dict.items(), key=operator.itemgetter(1), reverse=True))
    return sorted_dict


def generate_director_bar():
    """生成导演统计直方图"""
    directors = {k: v for k, v in get_director_statistics().items() if v >= 3}
    bar = pygal.Bar(my_config, style=my_style)
    bar.title = "IMDB TOP250 Director Statistics"
    bar.y_title = "Movies Count"
    bar.x_labels = directors.keys()
    bar.add("", values=directors.values())
    bar.render_to_file(output_path + "directors.svg")


def get_all_writers():
    """获取全部编剧"""
    all_writers = set()
    for movie in top250.find():
        for writer in movie['writers']:
            all_writers.add(writer)
    return all_writers


def get_writers_statistics():
    """统计每个编剧在TOP250的电影数量"""

    # 初始化
    writers_dict = {}
    all_writers = get_all_writers()
    for writers in all_writers:
        writers_dict[writers] = 0

    # 统计每部电影
    for movie in top250.find():
        for writers in movie['writers']:
            writers_dict[writers] = writers_dict[writers] + 1
    sorted_dict = dict(sorted(writers_dict.items(), key=operator.itemgetter(1), reverse=True))
    return sorted_dict


def generate_writers_bar():
    """生成编剧统计直方图"""
    writers = {k: v for k, v in get_writers_statistics().items() if v >= 3}
    bar = pygal.Bar(my_config, style=my_style)
    bar.title = "IMDB TOP250 Writer Statistics"
    bar.y_title = "Movies Count"
    bar.x_labels = writers.keys()
    bar.add("", values=writers.values())
    bar.render_to_file(output_path + "writers.svg")


def get_all_actors():
    """获取全部演员"""
    all_actors = set()
    for movie in top250.find():
        for actor in movie['actors']:
            all_actors.add(actor)
    return all_actors


def get_actors_statistics():
    """统计每个演员在TOP250的电影数量"""

    # 初始化
    actors_dict = {}
    all_actors = get_all_actors()
    for actor in all_actors:
        actors_dict[actor] = 0

    # 统计每部电影
    for movie in top250.find():
        for actor in movie['actors']:
            actors_dict[actor] = actors_dict[actor] + 1
    sorted_dict = dict(sorted(actors_dict.items(), key=operator.itemgetter(1), reverse=True))
    return sorted_dict


def generate_actors_bar():
    """生成演员统计直方图"""
    actors = {k: v for k, v in get_actors_statistics().items() if v >= 4}
    bar = pygal.Bar(my_config, style=my_style)
    bar.title = "IMDB TOP250 Actor Statistics"
    bar.y_title = "Movies Count"
    bar.x_labels = actors.keys()
    bar.add("", values=actors.values())
    for key in actors.keys():
        print(key)
    bar.render_to_file(output_path + "actors.svg")


def get_all_languages():
    """获取全部语言"""
    all_languages = set()
    for movie in top250.find():
        for language in movie['language']:
            all_languages.add(language)
    return all_languages


def get_language_statistics():
    """统计每种语言在TOP250的电影数量"""

    # 初始化
    language_dict = {}
    all_language = get_all_languages()
    for language in all_language:
        language_dict[language] = 0

    # 统计每部电影
    for movie in top250.find():
        for language in movie['language']:
            language_dict[language] = language_dict[language] + 1
    sorted_dict = dict(sorted(language_dict.items(), key=operator.itemgetter(1), reverse=True))
    return sorted_dict


def generate_language_bar():
    """生成语言统计直方图"""
    languages = {k: v for k, v in get_language_statistics().items() if v >= 2}
    bar = pygal.Bar()
    bar.title = "IMDB TOP250 Language Statistics"
    for k, v in languages.items():
        bar.add(k, v)
    bar.render_to_file(output_path + "languages.svg")


def max_run_time_top_10():
    """时间最长的十部电影"""
    movies = top250.find().sort("max_runtime", pymongo.DESCENDING).limit(10)
    movies_dict = {}
    for movie in movies:
        movies_dict[movie['title']] = movie['max_runtime']
    return movies_dict


def generate_max_run_time_top_10_bar():
    """生成类型统计直方图"""
    movies_dict = max_run_time_top_10()
    bar = pygal.Bar(my_config, style=my_style)
    bar.title = "IMDB Rating Max Runtime TOP10 Statistics"
    bar.y_title = "Movies Time(min)"

    bar.x_labels = movies_dict.keys()
    bar.add("", values=movies_dict.values())

    bar.render_to_file(output_path + "max_run_time_top10.svg")


def min_run_time_top_10():
    """时间最短的十部电影"""
    movies = top250.find().sort("min_runtime").limit(20)
    movies_dict = {}
    count = 0
    for movie in movies:
        if 'min_runtime' in movie.keys():
            movies_dict[movie['title']] = movie['min_runtime']
            count = count + 1
        if count >= 10:
            break
    return movies_dict


def generate_min_run_time_top_10_bar():
    """生成类型统计直方图"""
    movies_dict = min_run_time_top_10()
    bar = pygal.Bar(my_config, style=my_style)
    bar.title = "IMDB Rating Min Runtime TOP10 Statistics"
    bar.y_title = "Movies Time(min)"

    bar.x_labels = movies_dict.keys()
    bar.add("", values=movies_dict.values())

    bar.render_to_file(output_path + "min_run_time_top10.svg")

# 国家
# generate_all_countries_bar()
# generate_country_bar_without_usa()

# 年份
# generate_years_line()

# 年代
# generate_generation_bar()

# 类型
# generate_genre_bar()

# 评价人数
# generate_rating_count_top_10_bar()

# 导演
# generate_director_bar()

# 编剧
# generate_writers_bar()

# 演员
# generate_actors_bar()

# 语言
# generate_language_bar()

# 时间
# generate_max_run_time_top_10_bar()
# generate_min_run_time_top_10_bar()
