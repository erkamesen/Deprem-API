# Deprem API
a flask based API where you can do earthquake queries 
from Kandilli Rasathanesi

## ENDPOINTS

### /earthquakes

<table>
                    <tr>
                        <td>api_key</td>
                        <td>required*</td>
                        <td>string</td>
                        <td>Abone olup mail yoluyla alabilirsiniz.</td>
                    </tr>
                    <tr>
                        <td>min</td>
                        <td>optional</td>
                        <td>float</td>
                        <td>Depremleri filtrelemek için minimum bir değer giriniz.</td>
                    </tr>
                    <tr>
                        <td>max</td>
                        <td>optional</td>
                        <td>float</td>
                        <td>Depremleri filtrelemek için maximum bir değer giriniz.</td>
                    </tr>
                    <tr>
                        <td>order_by</td>
                        <td>optional</td>
                        <td>string</td>
                        <td>Depremleri belli şartlara göre artan yada azalan değerde sıralamak için kullanılır.<br>
                            Alabileceği değerler: <br> "intensity" => Şiddetlere göre sıralar. <br> "depth" => Derinliğe
                            göre sıralar.
                        </td>
                    </tr>
                    <tr>
                        <td>order</td>
                        <td>optional</td>
                        <td>string</td>
                        <td>Eğer order_by kullanıldıysa sıralamanın yönünü belirtmek için kullanılır.Default olarak
                            artan yöndedir. <br> Alabileceği değerler: <br> "ascending", "descanding"

</td>
</tr>
</table>

request:
```
curl http://127.0.0.1:5000/earthquakes?api_key=a6499dd44b4697afe9a9d8ab585a78dd&min=1&max=2
```
response:
```
 [{"control":"İlksel","coordinate":{"latitude":38.4523,"longitude":37.342},"depth":8.5,"id":1, "intensity":{"MD":"-.-","ML":"1.6","MW":"-.-"}, "location":"GAZIKOY-DARENDE (MALATYA)", "time":{"date":"2023.04.12","hour":"04:00:22"}}, ...
```

### earthquakes/< id >


<table>
                    <tr>
                        <td>api_key</td>
                        <td>required*</td>
                        <td>string</td>
                        <td>Abone olup mail yoluyla alabilirsiniz.</td>
                    </tr>
</table>

request:
```
curl http://127.0.0.1:5000/earthquakes/10
```

response:
```
{"control":"İlksel","coordinate":{"latitude":38.2577,"longitude":36.0708},"depth":5.0,"id":10,"intensity":{"MD":"-.-","ML":"1.7","MW":"-.-"},"location":"DEMIROLUK-TUFANBEYLI (ADANA)","time":{"date":"2023.04.12","hour":"03:42:28"}}

```

### earthquakes/< city >

<table>
                    <tr>
                        <td>api_key</td>
                        <td>required*</td>
                        <td>string</td>
                        <td>Abone olup mail yoluyla alabilirsiniz.</td>
                    </tr>
                    <tr>
                        <td>min</td>
                        <td>optional</td>
                        <td>float</td>
                        <td>Depremleri filtrelemek için minimum bir değer giriniz.</td>
                    </tr>
                    <tr>
                        <td>max</td>
                        <td>optional</td>
                        <td>float</td>
                        <td>Depremleri filtrelemek için maximum bir değer giriniz.</td>
                    </tr>
                    <tr>
                        <td>order_by</td>
                        <td>optional</td>
                        <td>string</td>
                        <td>Depremleri belli şartlara göre artan yada azalan değerde sıralamak için kullanılır.<br>
                            Alabileceği değerler: <br> "intensity" => Şiddetlere göre sıralar. <br> "depth" => Derinliğe
                            göre sıralar. <br> "distance" => Mesafeye göre sıralar.
                        </td>
                    </tr>
                    <tr>
                        <td>order</td>
                        <td>optional</td>
                        <td>string</td>
                        <td>Eğer order_by kullanıldıysa sıralamanın yönünü belirtmek için kullanılır.Default olarak
                            artan yöndedir. <br> Alabileceği değerler: <br> "ascending", "descanding"

</td>
</tr>
</table>

request:
```
curl http://127.0.0.1:5000/earthquakes/istanbul
```
response:
```
[{"control":"\u0130lksel","coordinate":{"latitude":40.8027,"longitude":29.2665},"depth":3.9,"id":480,"intensity":{"MD":"-.-","ML":"1.4","MW":"-.-"},"location":"TUZLA (ISTANBUL)","time":{"date":"2023.04.09","hour":"08:59:42"}}]
```

