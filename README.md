# structure

---

* ./app - django app
* ./turk - set of selectors to retrieve some translations, shall only contain logic for retrieval / insertion of words + translations
* ./scrap - service that scraps words/sentences n stuff from the web (I think, that wiki shall good enough for starters).

# todo

---

* [ ] telegram chat bot
  * [ ] /start
    * register and track user + chat somewhere in db
  * [ ] /quiz:
    * post some message by bot having some inline quiz, like:

        <div>
            <h6>Choose correct translation for word <b>bir</b>:</h6>

        <table>

            <tr>
                <td>Один</td>
                <td>Два </td>
                <td>Три</td>
                <td>Там</td>
            </tr>
        </table>
        </div>

        ---

        -> correct:
            next quiz
        -> incorrect:
            post a word, with translation and examples.
  * [ ] /add
    * allow user to propose a word with given translation.
  * [ ] /stats
    * show users current statistics (correct answers and so on)

* [ ] web app (most probably django, to overview stats, add content)
* [ ] scrapy service, with spiders, to scrap forums/sites and extract text out of them, to get statistics analysis of most common current words
