#  SomaFMPlayer

[SomaFM](https://somafm.com/) has been a near-constant companion for background music, and new artist discoveries for me for at least the last 15 years. 

This is a  little ditty to use Flask to launch my favourite SomaFM radio streams. No AirPlay, no casting, just launch/stream/play directly from the RPi using simple REST-esque calls.

Although it can be triggered to start a stream using a browser or even CURL (like '$ curl http://claire.kenkl.org:5000/play?stream=DroneZone'), I've also assembled a companion application - [somafmcontroller](https://github.com/kenkl/somafmcontroller) to select the stream, change volume, or even stop the stream.


2021-06-12: Refactored a bit to grab the full list of streams on startup and play from the stream id provided.


