import asyncio

import discord
import psycopg2
from discord.ext import commands


async def add_db(string):
    db = psycopg2.connect(host="ec2-44-195-201-3.compute-1.amazonaws.com",
                          database="d3bjgaf44oicgk",
                          password="b1696d318ff8248df9aabf877f63ea752bc031be899b0408b935da4cb730d1c9",
                          port=5432, user="qygylrtrevsqcy")
    cur = db.cursor()
    cur.execute(f"INSERT INTO term_link_db(string) VALUES({string.strip()});")
    db.commit()
    cur.close()
    db.close()


async def delete_db(term):
    db = psycopg2.connect(host="ec2-44-195-201-3.compute-1.amazonaws.com",
                          database="d3bjgaf44oicgk",
                          password="b1696d318ff8248df9aabf877f63ea752bc031be899b0408b935da4cb730d1c9",
                          port=5432, user="qygylrtrevsqcy")
    cur = db.cursor()
    cur.execute(f"DELETE FROM public.term_link_db WHERE string={term.strip()};")
    db.commit()
    cur.close()
    db.close()


class general(commands.Cog, name="addTerm"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addterm", description="Add a new term to database. Syntax: e!addterm [term] [link]")
    @commands.has_role("Leader")
    async def add_term(self, context, term, link):
        await asyncio.gather(await add_db(f"{term.strip()}<>{link.strip()}"))
        await context.send(
            embed=discord.Embed(description=f"The term `{term}' has been added to the database!",
                                color=0xD5059D))

    @commands.command(name="deleteterm", description="Delete a term from the database. Syntax: e!deleteterm [term] [link]")
    @commands.has_role("Leader")
    async def delete_term(self, context, term):
        await asyncio.gather(await delete_db(term))
        await context.send(embed=discord.Embed(description=f"The term `{term}' has been deleted from the database!",
                                               color=0xD5059D))


def setup(bot):
    bot.add_cog(general(bot))
