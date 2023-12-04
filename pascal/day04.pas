program Day04;

type
  BitSet = array[0..15] of byte;

procedure SetBit(var bs: BitSet; n: integer);
var
  index: integer;
begin
  index := n div 8;
  bs[index] := bs[index] or (1 shl (n mod 8));
end;

function CountMatches(a, b: BitSet): integer;
var
  i, j: integer;
  n: integer;
begin
  n := 0;
  for i := 0 to 15 do
  begin
    a[i] := a[i] and b[i];
    for j := 0 to 7 do if (a[i] and (1 shl j)) <> 0 then inc(n);
  end;
  CountMatches := n;
end;

var
  f: text;
  counts: array[0..219] of longint;
  i, j, n, code: integer;
  winning, own: BitSet;
  line: string;
  number: string;
  sum: longint;

begin
  Assign(f, '..\inputs\04.txt');
  Reset(f);
  sum := 0;
  for i := 0 to 219 do
  begin
    ReadLn(f, line);
    for j := 0 to 15 do
    begin
      winning[j] := 0;
      own[j] := 0;
    end;
    for j := 0 to 9 do
    begin
      number := Copy(line, 11 + j * 3, 2);
      Val(number, n, code);
      SetBit(winning, n);
    end;
    for j := 0 to 24 do
    begin
      number := Copy(line, 43 + j * 3, 2);
      Val(number, n, code);
      SetBit(own, n);
    end;

    n := CountMatches(winning, own);

    Inc(counts[i]);
    if n > 0 then
    begin
      Inc(sum, 1 shl (n-1));
      for j := 0 to n-1 do if i+j+1 < 220 then Inc(counts[i+j+1], counts[i]);
    end;

  end;
  WriteLn(sum);

  sum := 0;
  for i := 0 to 219 do Inc(sum, counts[i]);
  WriteLn(sum);
end.
