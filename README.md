# tool_gen_jv_xml
A small python tool to generat xml test fields as below format:  
```xml
  <!-- For jv test -->
  <Location name="data_dep_0">
    <address country="China" city="Shanghai" postalCode="" street="" houseNumber="" crossing="" />
    <position latitude="3119781" longitude="12147758" />
  </Location>
  <Location name="data_des_0">
    <address country="China" city="Shanghai" postalCode="" street="" houseNumber="" crossing="" />
    <position latitude="3119679" longitude="12147707" />
  </Location>
```

The input file content example:  
```
This is first line in input file, first line will be ignored
*AnyChar*(3119781, 12147758)*AnyChar*(3119679, 12147707)*AnyChar*
*AnyChar*(3123469, 12151116)*AnyChar*(3123335, 12150893)*AnyChar*
```
For each line, the first (x1, y1) will be departure coordinate, the second (x2, y2) will be departure coordinate  

