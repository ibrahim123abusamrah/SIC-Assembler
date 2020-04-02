COPY     START  1000                    .comment
FIRST    STL    RETADR
CLOOP    JSUB   RDREC
  -      LDA    =C'EOF'
  -      COMP   ZERO
  -      JEQ    ENDFIL
  -      JSUB   WRREC
  -      J      CLOOP
ENDFIL   LDA    EOF
  -      LTORG
  -      STA    BUFFER
  -      LDA    THREE
  -      STAd   LENGTH
  -      JSUB   WRREC
  -      LDL    RETADR
  -      RSUB
EOF      BYTE   C'EOF'
THREE    WORD   3
ZERO     WORD   0
RETADR   RESW   1
LENGTH   RESW   1
BUFFER   RESB   4096
.
.      SUBROUTINE TO READ RECORD INTO BUFFER
.
RDREC    LDX    ZERO
  -      LDA    =X'0052'
RLOOP    TDf    INPUT
  -      JEQ    RLOOP
  -      RD     INPUT
  -      COMP   ZERO
  -      JEQ    EXIT
  -      LTORG
  -      STCH   BUFFER,X
  -      TIX    MAXLEN
  -      JLT    RLOOP
EXIT     STX    LENGTH
         RSUB
INPUT    BYTE   X'F1'
MAXLEN   WORD   4096
.
.      SUBROUTINE TO WRITE RECORD FROM BUFFER
.
WRREC    LDX    ZERO
WLOOP    TD     OUTPUT
  -      JEQ    WLOOP
  -      LDCH   BUFFER,X
  -      WD     OUTPUT
  -      TIX    LENGTH
  -      JLT    WLOOP
  -      RSUB
OUTPUT   BYTE   X'06'
  -      END    FIRST
