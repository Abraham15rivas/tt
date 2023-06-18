# Talky Trader
![CEX & DEX integration with messaging platform and plugin support.](https://readme-typing-svg.demolab.com?font=Fira+Code&size=13&duration=2000&pause=100&color=027CF9&multiline=true&repeat=false&width=600&height=60&lines=Connect+CEX+and+DEX+exchanges+across+multi+messaging+platforms.;Place+order%2C+inquire+your+balance+and+more+through+plugins.;Easily+deploy+via+Docker+on+self-hosted+platforms+or+PaaS.)

[![Docker Pulls](https://badgen.net/docker/pulls/mraniki/tt)](https://hub.docker.com/r/mraniki/tt)<br> [![wiki](https://img.shields.io/badge/🪙🗿-wiki-027CF9)](https://talkytrader.gitbook.io/talky/)

[![Logo](https://i.imgur.com/Q7iDDyB.jpg)](https://github.com/mraniki/tt)
 </tr>
<details>
<summary><h2>Quick start</h2></summary>


 <h3>Install</h3>

1) Create your channel/room and your platform bot

    - Telegram via [Telegram @BotFather](https://core.telegram.org/bots/tutorial) and [create an API key](https://docs.telethon.dev/en/stable/basic/signing-in.html) 
    - Discord via [Discord Dev portal](https://discord.com/developers/docs/intro)
    - Matrix via [Matrix.org](https://turt2live.github.io/matrix-bot-sdk/index.html)

2) Get your

    - CEX API Keys supported by [CCXT](https://github.com/ccxt/ccxt) or
    - DEX wallet address and private key

3) Create your config [/app/settings.toml](src/example_settings.toml)

4) Deploy via:
    - docker `docker push mraniki/tt:latest` or `docker pull ghcr.io/mraniki/tt:latest`
    - locally `git clone https://github.com/mraniki/tt:main` && `pip install -r requirements.txt`

5) Start your container or if deployed locally use `python3 bot.py` to start

6) More details in [Wiki](https://github.com/mraniki/tt/wiki)


 <h3>Build status</h3>

[![codecov](https://codecov.io/gh/mraniki/tt/branch/main/graph/badge.svg?token=ILJTC0F4K1)](https://codecov.io/gh/mraniki/tt)

[![👷Flow](https://github.com/mraniki/tt/actions/workflows/%F0%9F%91%B7Flow.yml/badge.svg)](https://github.com/mraniki/tt/actions/workflows/%F0%9F%91%B7Flow.yml)


![Alt](https://repobeats.axiom.co/api/embed/a2d03eaf66dab33c82d52170d8ebfb0c479590a9.svg "Repobeats analytics image")

 
<h3> Libraries </h3>

[![python3.10](https://badgen.net/badge/icon/3.10/black?icon=pypi&label)](https://www.python.org/downloads/release/python-3100/)
[![ccxt](https://badgen.net/badge/icon/ccxt/black?icon=libraries&label)](https://github.com/ccxt/ccxt)
[![dxsp](https://badgen.net/badge/icon/dxsp?icon=pypi&label)](https://pypi.org/project/dxsp/)
[![findmyorder](https://badgen.net/badge/icon/findmyorder?icon=pypi&label)](https://pypi.org/project/findmyorder/)
[![iamlistening](https://badgen.net/badge/icon/iamlistening?icon=pypi&label)](https://pypi.org/project/iamlistening/)
[![talkytrend](https://badgen.net/badge/icon/talkytrend?icon=pypi&label)](https://pypi.org/project/talkytrend/)

[![apprise](https://badgen.net/badge/icon/apprise/black?icon=libraries&label)](https://github.com/caronc/apprise) [![FastAPI](https://badgen.net/badge/icon/fastapi/black?icon=libraries&label)](https://github.com/tiangolo/fastapi)
</details> 

<h3><a href="https://github.com/mraniki/tt/wiki/Screenshots">📷 Screenshots</a></h3>
<img width="194" alt="222953459-0aaf024b-4d7b-4a57-b31b-7cab08f3c0d3" src="https://github.com/mraniki/tt/assets/8766259/14cb1653-f6b4-44e7-b07c-d930060c7363">
