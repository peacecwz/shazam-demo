# Shazam Demo

This project is about Shazam Demo. You are going to learn how to analyze and index musics to database and search for musics in database.

## Installing

First of all, you should have installed Python version 2.7 and pip.

```
pip install numpy termcolor pyaudio wave pydub
```

## How to use

1. Run reset.py file to clear and re-initialize your database

```
python reset.py
```

2. Put your mp3 files into mp3 folder
3. Run analyze.py 

```
python analyze.py
```

4. When you see indexed musics to database and run listen.py to listen music to discover. You will have to pass a second parameter for listening offset (by default it is 10 seconds)

```
python listen.py -s 5
```

5. Done!

## How is it work

I have written an article with "How Shazam's audio search algorithm works?" title. You may read it at [here](http://devnot.com/2018/shazam-in-muzik-arama-algoritmasi-nasil-calisir/) (Article is in Turkish. You may try Google, Yandex or Bing Translation.)

## Dependencies

* Python 2.7
* numpy 
* termcolor 
* pyaudio
* wave
* pydub

## Contributing

* If you want to contribute to codes, create pull request
* If you find any bugs or error, create an issue

## License

This project is licensed under the MIT Lıcense
