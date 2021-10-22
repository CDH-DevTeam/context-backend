from django.db import models

# Token models
class Lemma(models.Model): 
    # A lemma is the lower-case base form of a token
    # e.g. "car" from "Cars"

    text = models.CharField(max_length=128, primary_key=True)

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return str(self)

class Word(models.Model):
    # A word is the lower-case form of a token as it appears in text,
    # e.g. "cars" from "Cars"

    text = models.CharField(max_length=128, primary_key=True)
    lemma = models.ForeignKey(Lemma, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return str(self)


# Document models
class Document(models.Model):
    
    name    = models.CharField(max_length=128, primary_key=True)
    chamber = models.CharField(max_length=2, default='')
    year    = models.PositiveIntegerField(default=0)
    n_words = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:

        chamber = {'ak': 'Andra kammaren', 'fk': 'Första kammaren'}

        return f"{self.year}, {chamber.get(self.chamber)}, {self.name}"  

class Sentence(models.Model):

    id          = models.BigAutoField(primary_key=True)
    document    = models.ForeignKey(Document, on_delete=models.CASCADE)
    text        = models.TextField(default="")

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return str(self)

class Token(models.Model): 
    # A token is the appearance of words or symbols in the text,
    # where each appearance counts as unique
    # e.g. "Cars"

    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    word     = models.ForeignKey(Word, on_delete=models.CASCADE)
    # text     = models.CharField(max_length=128, primary_key=True)

    def __str__(self) -> str:
        return self.word.text

    def __repr__(self) -> str:
        return str(self)
