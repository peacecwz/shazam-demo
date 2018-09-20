# Shazam Demo

This project is about Shazam Demo. How to analyze and index musics to database and search musics in database. I will add "How to use", "How is it working?" etc...

## Installing

First of all, you have to install Python 2.7 version and pip

```
pip install numpy termcolor pyaudio wave pydub
```

## How to use

1. Run reset.py file for clear and initialize your database

```
python reset.py
```

2. Put your mp3 files to mp3 folder
3. Run analyze.py 

```
python analyze.py
```

4. When you see indexed musics to database and run listen.py and open music for discovering. You have to pass second for listening offset (by default second is 10)

```
python listen.py -s 5
```

5. Done!

## How is it work

I have written an article about "How Shazam's audio search algorithm works?" You can see on ![here](http://devnot.com/2018/shazam-in-muzik-arama-algoritmasi-nasil-calisir/) (It's turkish article)

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
