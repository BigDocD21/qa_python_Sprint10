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

        assert len(collector.get_books_genre()) == expected_count


    def test_add_new_book_rejects_duplicate(self):
        collector = BooksCollector()

        book_name = "Геральт"

        collector.add_new_book(book_name)
        collector.add_new_book(book_name)

        assert len(collector.get_books_genre()) == 1


    def test_set_book_genre_updates_genre(self):
        collector = BooksCollector()

        book_name = "Песнь льда и пламени"
        genre = "Фантастика"

        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)

        assert collector.get_book_genre(book_name) == genre


    def test_set_book_genre_rejects_invalid_genre(self):
        collector = BooksCollector()

        book_name = "Тайная комната"
        invalid_genre = "неизвестный жанр"

        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, invalid_genre)
        
        assert collector.get_book_genre(book_name) == ''

    def test_get_books_with_specific_genre_returns_matching_books(self):
        collector = BooksCollector()
        
        collector.add_new_book("Книга А")
        collector.add_new_book("Книга Б")
        collector.set_book_genre("Книга А", "Фантастика")
        collector.set_book_genre("Книга Б", "Фантастика")
        
        result = collector.get_books_with_specific_genre("Фантастика")
        
        assert "Книга А" in result
        assert "Книга Б" in result


    def test_get_books_with_specific_genre_returns_empty_for_unknown(self):
        collector = BooksCollector()
        
        collector.add_new_book("Книга В")
        collector.set_book_genre("Книга В", "Фантастика")
        
        result = collector.get_books_with_specific_genre("Ужасы")
        
        assert len(result) == 0



    @pytest.mark.parametrize("restricted_genre", ['Ужасы', 'Детективы'])
    def test_get_books_for_children_excludes_restricted_genres(self, restricted_genre):
        collector = BooksCollector()

        book_name = "Воспламеняющая взглядом"

        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, restricted_genre)

        children_books = collector.get_books_for_children()

        assert book_name not in children_books


    def test_add_book_in_favorites_successfully_adds_book(self):
        collector = BooksCollector()

        book_name = "Ведьмак"

        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)

        favorites = collector.get_list_of_favorites_books()

        assert book_name in favorites


    def test_add_book_in_favorites_rejects_duplicate(self):
        collector = BooksCollector()

        book_name = "Владычица Озер"

        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.add_book_in_favorites(book_name)

        favorites = collector.get_list_of_favorites_books()

        assert len(favorites) == 1



    def test_delete_book_from_favorites_removes_book(self):

        collector = BooksCollector()
        book_name = "Палата № 6"
        
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        
        favorites = collector.get_list_of_favorites_books()

        assert book_name not in favorites

    def test_delete_book_from_favorites_handles_missing_book(self):

        collector = BooksCollector()

        collector.delete_book_from_favorites("Не существующая книга")
        
        favorites = collector.get_list_of_favorites_books()

        assert len(favorites) == 0

    def test_new_book_has_empty_genre_initially(self):
        collector = BooksCollector()

        book_name = "Новая книга"
        
        collector.add_new_book(book_name)
        genre = collector.get_book_genre(book_name)
        
        assert genre == ''
