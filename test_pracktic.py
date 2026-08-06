import pytest
from main import BooksCollector


class TestBooksCollector:

    def test_add_new_book_add_two_books(self):

        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')


        assert len(collector.get_books_genre()) == 2

    @pytest.mark.parametrize("book_name, should_be_added", [
        ('A' * 40, True),
        ('Териминатор', True), 
        ('A' * 41, False),
        ('', False),
        ('A' * 100, False),
    ])
    def test_add_new_book_length_validation(self, book_name, should_be_added):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        
        books_dict = collector.get_books_genre()
        current_names = list(books_dict.keys())
        
        if should_be_added:
            assert len(books_dict) == 1
            assert book_name in current_names
        else:
            assert len(books_dict) == 0
            assert book_name not in current_names

    @pytest.mark.parametrize("name1, name2, expected_count", [
        ("Геральт", "Геральт", 1),
        ("Геральт", "1976", 2),
        ("A" * 40, "A" * 40, 1),
    ])
    def test_add_new_book_handles_duplicates(self, name1, name2, expected_count):
        collector = BooksCollector()
        
        collector.add_new_book(name1)
        collector.add_new_book(name2)
        
        books_dict = collector.get_books_genre()
        current_names = list(books_dict.keys())
        
        assert len(books_dict) == expected_count
        
        if name1 == name2:
            assert current_names.count(name1) == 1
        else:
            assert name1 in current_names
            assert name2 in current_names 


    def test_set_genre_and_find_by_genre(self):
        collector = BooksCollector()
        book_name = "Песнь льда и пламени"
        genre = "Фантастика"
        
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        
        assert collector.get_book_genre(book_name) == genre
        
        books_in_genre = collector.get_books_with_specific_genre(genre)
        assert book_name in books_in_genre
        
        other_genre = "Ужасы"
        books_in_other_genre = collector.get_books_with_specific_genre(other_genre)
        assert book_name not in books_in_other_genre 


    @pytest.mark.parametrize("restricted_genre", ['Ужасы', 'Детективы'])
    def test_get_books_for_children_excludes_restricted_genres(self, restricted_genre):
        collector = BooksCollector()
        book_name = "Воспламеняющая взглядом"
        
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, restricted_genre)
        
        children_books = collector.get_books_for_children()
        
        assert book_name not in children_books, (
            f"Ошибка! Книга '{book_name}' с жанром '{restricted_genre}' "
            f"попала в подборку для детей."
        ) 


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
        
        assert genre == '', f"Ожидался пустой жанр сразу после добавления, а получено: '{genre}'"

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
        