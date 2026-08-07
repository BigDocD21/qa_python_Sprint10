import pytest
from main import BooksCollector


class TestBooksCollector:

    def test_add_new_book_add_two_books(self):

        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')


        assert len(collector.get_books_genre()) == 2

    @pytest.mark.parametrize("book_name, expected_count", [
        ('A' * 40, 1),
        ('Териминатор', 1),
        ('A' * 41, 0),
        ('', 0),
        ('A' * 100, 0),
    ])


    def test_add_new_book_length_validation(self, book_name, expected_count):
        collector = BooksCollector()

        collector.add_new_book(book_name)
        books_dict = collector.get_books_genre()

        assert len(books_dict) == expected_count


    def test_add_new_book_rejects_duplicate(self):
        collector = BooksCollector()

        book_name = "Геральт"

        collector.add_new_book(book_name)
        collector.add_new_book(book_name)

        books_dict = collector.get_books_genre()

        assert len(books_dict) == 1
        assert book_name in books_dict.keys()


    def test_add_new_book_adds_different_books(self):
        collector = BooksCollector()

        name1 = "Геральт"
        name2 = "Йеннифер"

        collector.add_new_book(name1)
        collector.add_new_book(name2)

        books_dict = collector.get_books_genre()

        assert len(books_dict) == 2
        assert name1 in books_dict.keys()
        assert name2 in books_dict.keys()


    def test_set_book_genre_updates_genre(self):
        collector = BooksCollector()

        book_name = "Песнь льда и пламени"
        genre = "Фантастика"

        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)

        assert collector.get_book_genre(book_name) == genre


    def test_get_books_with_specific_genre_filters_correctly(self):
        collector = BooksCollector()

        book_name = "Песнь льда и пламени"
        genre = "Фантастика"
        other_genre = "Ужасы"

        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)

        books_in_genre = collector.get_books_with_specific_genre(genre)
        books_in_other_genre = collector.get_books_with_specific_genre(other_genre)

        assert book_name in books_in_genre
        assert book_name not in books_in_other_genre


    @pytest.mark.parametrize("restricted_genre", ['Ужасы', 'Детективы'])


    def test_get_books_for_children_excludes_restricted_genres(self, restricted_genre):
        collector = BooksCollector()

        book_name = "Воспламеняющая взглядом"

        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, restricted_genre)

        children_books = collector.get_books_for_children()

        assert book_name not in children_books


    def test_add_and_get_favorites(self):
        collector = BooksCollector()

        book_name = "Ведьмак"

        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)

        favorites = collector.get_list_of_favorites_books()

        assert book_name in favorites
        assert len(favorites) == 1


    def test_delete_from_favorites(self):
        collector = BooksCollector()

        book_name = "Владычица Озер"

        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)

        favorites = collector.get_list_of_favorites_books()

        assert book_name not in favorites
        assert len(favorites) == 0

        collector.delete_book_from_favorites("Не существующая книга")

        assert len(favorites) == 0

    def test_new_book_has_no_genre_initially(self):
        collector = BooksCollector()

        book_name = "Новая книга"

        collector.add_new_book(book_name)
        genre = collector.get_book_genre(book_name)

        assert genre == ''


    def test_add_book_in_favorites_unique(self):
        collector = BooksCollector()

        book_name = "Ведьмак"

        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)

        favorites_first = collector.get_list_of_favorites_books()

        assert len(favorites_first) == 1
        
        collector.add_book_in_favorites(book_name)

        favorites_second = collector.get_list_of_favorites_books()
        
        assert len(favorites_second) == 1
        assert favorites_first == favorites_second 
