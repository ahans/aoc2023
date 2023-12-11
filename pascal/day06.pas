program Day06_Wait_for_it;

uses math;

var
  times: array of real;
  distances: array of real;

function Solve(time, distance: real): real;
var x1, x2: real;
begin
  x1 := (time + Sqrt(time * time - 4 * distance - 1e-9)) / 2.0;
  x2 := (time - Sqrt(time * time - 4 * distance - 1e-9)) / 2.0;
  Solve := Floor(x1) - Ceil(x2) + 1;
end;

var
  i: integer;
  p1: real;

begin
  { Input data, last item is part 2 }
  times :=     [7,  15,   30,  71530];
  distances := [9,  40,  200, 940200];

  p1 := 1;
  for i := 0 to Length(times)-2 do p1 := p1 * Solve(times[i], distances[i]);
  WriteLn(p1:0:0);
  WriteLn(Solve(times[Length(times)-1], distances[Length(distances)-1]):0:0);
end.

