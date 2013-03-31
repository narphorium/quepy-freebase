#!/usr/bin/env python
# coding: utf-8

# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Shawn Simister <simister@google.com>

"""
Freebase film domain semantics.
"""

from refo import Plus, Question
from quepy.semantics import HasKeyword
from quepy.semantics import FixedType, HasKeyword, FixedRelation, \
                            FixedDataRelation
from quepy.regex import Lemma, Lemmas, Pos, RegexTemplate, Particle
from semantics import NameOf, LabelOf, HasName, DefinitionOf
from people import IsPerson

nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

# Film types

class IsActor(FixedType):
    fixedtype = "freebase:film.actor"


class IsDirector(FixedType):
    fixedtype = "freebase:film.director"


class IsFilm(FixedType):
    fixedtype = "freebase:film.film"


# Film relations

class ProducedBy(FixedRelation):
    relation = "freebase:film.film.produced_by"


class ReleaseDateOf(FixedRelation):
    relation = "freebase:film.film.release_date"
    reverse = True


class StarsIn(FixedRelation):
    relation = "freebase:film.film.starring"
    reverse = True


class HasActor(FixedRelation):
    relation = "freebase:film.film.starring"


class DirectedBy(FixedRelation):
    relation = "freebase:film.film.directed_by"


class DirectorOf(FixedRelation):
    relation = "freebase:film.film.directed_by"
    reverse = True


class DurationOf(FixedRelation):
    relation = "freebase:film.film.runtime"
    reverse = True


class LocationOf(FixedRelation):
    relation = "freebase:film.film.featured_film_locations"
    reverse = True


# Film regular expressions

class Movie(Particle):
    regex = Question(Pos("DT")) + nouns

    def semantics(self, match):
        name = match.words.tokens
        return IsFilm() + HasName(name)


class Actor(Particle):
    regex = nouns

    def semantics(self, match):
        name = match.words.tokens
        return IsActor() + HasKeyword(name)


class Director(Particle):
    regex = nouns

    def semantics(self, match):
        name = match.words.tokens
        return IsDirector() + HasKeyword(name)


class ListMoviesRegex(RegexTemplate):
    """
    Ex: "list movies"
    """

    regex = Lemma("list") + (Lemma("movie") | Lemma("film"))

    def semantics(self, match):
        movie = IsFilm()
        name = NameOf(movie)
        return name, "enum"


class MoviesByDirectorRegex(RegexTemplate):
    """
    Ex: "List movies directed by Quentin Tarantino.
        "movies directed by Martin Scorsese"
        "which movies did Mel Gibson directed"
    """

    regex = (Question(Lemma("list")) + (Lemma("movie") | Lemma("film")) +
             Question(Lemma("direct")) + Lemma("by") + Director()) | \
            (Lemma("which") + (Lemma("movie") | Lemma("film")) + Lemma("do") +
             Director() + Lemma("direct") + Question(Pos(".")))

    def semantics(self, match):
        movie = IsFilm() + DirectedBy(match.director)
        movie_name = LabelOf(movie)

        return movie_name, "enum"


class MovieDurationRegex(RegexTemplate):
    """
    Ex: "How long is Pulp Fiction"
        "What is the duration of The Thin Red Line?"
    """

    regex = ((Lemmas("how long be") + Movie()) |
            (Lemmas("what be") + Pos("DT") + Lemma("duration") +
             Pos("IN") + Movie())) + \
            Question(Pos("."))

    def semantics(self, match):
        duration = DurationOf(match.movie)
        return duration, ("literal", "{} minutes long")


class ActedOnRegex(RegexTemplate):
    """
    Ex: "List movies with Hugh Laurie"
        "Movies with Matt LeBlanc"
        "In what movies did Jennifer Aniston appear?"
        "Which movies did Mel Gibson starred?"
        "Movies starring Winona Ryder"
    """

    acted_on = (Lemma("appear") | Lemma("act") | Lemma("star"))
    movie = (Lemma("movie") | Lemma("movies") | Lemma("film"))
    regex = (Question(Lemma("list")) + movie + Lemma("with") + Actor()) | \
            (Question(Pos("IN")) + (Lemma("what") | Lemma("which")) +
             movie + Lemma("do") + Actor() + acted_on + Question(Pos("."))) | \
            (Question(Pos("IN")) + Lemma("which") + movie + Lemma("do") +
             Actor() + acted_on) | \
            (Question(Lemma("list")) + movie + Lemma("star") + Actor())

    def semantics(self, match):
        movie = IsFilm() + HasActor(match.actor)
        movie_name = NameOf(movie)
        return movie_name, "enum"


class MovieReleaseDateRegex(RegexTemplate):
    """
    Ex: "When was The Red Thin Line released?"
        "Release date of The Empire Strikes Back"
    """

    regex = ((Lemmas("when be") + Movie() + Lemma("release")) |
            (Lemma("release") + Question(Lemma("date")) +
             Pos("IN") + Movie())) + \
            Question(Pos("."))

    def semantics(self, match):
        release_date = ReleaseDateOf(match.movie)
        return release_date, "literal"


class DirectorOfRegex(RegexTemplate):
    """
    Ex: "Who is the director of Big Fish?"
        "who directed Pocahontas?"
    """

    regex = ((Lemmas("who be") + Pos("DT") + Lemma("director") +
             Pos("IN") + Movie()) |
             (Lemma("who") + Lemma("direct") + Movie())) + \
            Question(Pos("."))

    def semantics(self, match):
        director = IsDirector() + DirectorOf(match.movie)
        director_name = NameOf(director)
        return director_name, "literal"


class ActorsOfRegex(RegexTemplate):
    """
    Ex: "who are the actors of Titanic?"
        "who acted in Alien?"
        "who starred in Depredator?"
        "Actors of Fight Club"
    """

    regex = (Lemma("who") + Question(Lemma("be") + Pos("DT")) +
             (Lemma("act") | Lemma("actor") | Lemma("star")) +
             Pos("IN") + Movie() + Question(Pos("."))) | \
            ((Lemma("actors") | Lemma("actor")) + Pos("IN") + Movie())

    def semantics(self, match):
        actor = NameOf(IsPerson() + StarsIn(match.movie))
        return actor, "enum"


class PlotOfRegex(RegexTemplate):
    """
    Ex: "what is Shame about?"
        "plot of Titanic"
    """

    regex = ((Lemmas("what be") + Movie() + Lemma("about")) | \
             (Question(Lemmas("what be the")) + Lemma("plot") +
              Pos("IN") + Movie()) +
            Question(Pos(".")))

    def semantics(self, match):
        definition = DefinitionOf(match.movie)
        return definition, "define"
