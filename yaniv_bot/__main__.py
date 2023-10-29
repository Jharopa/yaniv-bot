""" YanivBot """

from yaniv_bot.bot import YanivBot


def main() -> None:
    bot = YanivBot()

    bot.run(bot.config["token"])


if __name__ == "__main__":
    main()
