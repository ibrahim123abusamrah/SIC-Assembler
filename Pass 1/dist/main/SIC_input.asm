SUM      START   0
FIRST    LDX     #0                LOAD X REGISTER WITH 0
         LDA     #0                LOAD ACCUMULATOR WITH 0
         LDB     #TABLE2
LOOP     ADD     TABLE, X
         ADD     TABLE2, X
         TIX     COUNT
         JLT     LOOP
         STA     TOTAL
         RSUB                      RETURN TO CALLER
         .
         . This is a comment
         .
COUNT    RESW    1
COUNT    RESW    1
TABLE    RESW    2000              2000-WORD TABLE AREA
TABLE2   RESW    2000              2000-WORD TABLE2 AREA
TOTAL    RESW    1
         END     FIRST