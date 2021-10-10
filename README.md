# Varahenkilöpalvelu muusikoille


Sovellus on tarkoitettu muusikoille jotka etsivät yksittäisille keikoille soittajia/tuuraajia esiintymään tai keikkoja soittaakseen. Sovelluksessa käyttäjä voi rekisteröidä yhtyeensä (ja määritellä tarpeen eri instrumenttien soittajille) ja yhtyeelle keikkoja, johon eri käyttäjät voivat ilmoittautua tuuraamaan. Käyttäjä voi rekisteröityä palveluun myös rekisteröimättä mitään yhtyettä ja etsiä keikkoja soitettavaksi.
  
##### Välipalautus 3 ominaisuudet:

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen
- Käyttäjä näkee etusivulla listan keikoista (sisältää yhtyeen nimen, keikan päivämäärän, sijainnin, kuvauksen ja eri soittajien tarpeen)
- Käyttäjä voi lisätä itselleen yhtyeen ja ilmoittaa yhtyeelleen keikkoja johon tarvitaan soittajia
- Käyttäjä pystyy ilmoittautumaan itsensä keikalle tuuraajaksi
- Käyttäjä pystyy poistamaan omia yhtyeitään, keikkojaan ja ilmoittautumisiaan

## Relaatiokaavio

![alt text](https://github.com/Faktatykki/musician-reserve-service/blob/main/documentation/musician-reserve-schema.png)

## Huomioita arvioijalle

Ulkoisesti sovellus on vielä hyvin primitiivinen ja ohjelman ulkoasu päivittyy 1990-luvulta lähemmäksi nykypäivää loppupalautukseen mennessä

## Testaaminen 

Sovellusta voi testata Herokussa osoitteessa:

[Musician-reserve-service](https://musician-reserve-service.herokuapp.com/)

Tietokannasta löytyy tällä hetkellä kaksi käyttäjää:

Käyttäjänimi: Testi
Salasana: Testaaja

Käyttäjänimi: Testi2
Salasana: Testaaja2


Kannattaa testata käyttäjien, yhtyeiden ja keikkojen luomista kummallisilla syötteillä (erikoismerkkejä yms.)


Rattoisia testaamisia!









