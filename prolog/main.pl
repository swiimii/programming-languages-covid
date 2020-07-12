% swipl --quiet -s main.pl -t halt.
% swipl -s main.pl -g "main" -t halt.
% main:-
%     open('data/database.txt', read, Str),
%     read(Str, Line1),
%     close(Str),
%     write([Line1]), nl.

% https://stackoverflow.com/questions/4805601/read-a-file-line-by-line-in-prolog
main :-
    open('data/database.txt', read, Str),
    read_file(Str,Lines),
    close(Str),
    write(Lines), nl.

read_file(Stream,[]) :-
    at_end_of_stream(Stream).

read_file(Stream,[X|L]) :-
    \+ at_end_of_stream(Stream),
    read(Stream,X),
    read_file(Stream,L).
