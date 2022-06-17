(function(){
    if (window.myBookmarklet !== undefined){
        myBookmarklet();
    }
    else {
        document.body.appendChild(document.createElement('script')).src='https://127.0.0.1:8000/static/js/bookmarklet.js?r='+Math.floor(Math.random()*99999999999999999999);
    }
})();
//   /127.0.0.1:8000/    /mysite.com:8000/    /9a8419d646ac.ngrok.io/
//  Этот фрагмент проверяет, был ли уже загружен код букмарклета,
//  который хранится в переменной myBookmarklet
//  так мы измегаем лишней загрузки кода, в случае, когда пользователь
//  повторно кликает на букмареклет
//  если переменная myBookmarklet не содержит значения,
//  код загружает другой js-файл, добавляя <script> элемент в документ
//  тег <script> загружает bookmarklet.js, добавляя к наванию случайное число
//  это необъодимо для предотвращения кеширования файла браузером
//  актуальный код букмарклета будет находиться в bookmarklet.js
//  это позволит обновлять выполняемый код без необходимости для пользователя
//  обновлять закладку, которую он добавил ранее