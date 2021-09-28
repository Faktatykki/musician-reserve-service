# Varahenkilöpalvelu muusikoille


Sovellus on tarkoitettu muusikoille jotka etsivät yksittäisille keikoille soittajia/tuuraajia esiintymään tai keikkoja soittaakseen. Sovelluksessa käyttäjä voi rekisteröidä yhtyeensä (ja määritellä tarpeen eri instrumenttien soittajille) ja yhtyeelle keikkoja, johon eri käyttäjät voivat ilmoittautua tuuraamaan. Käyttäjä voi rekisteröityä palveluun myös rekisteröimättä mitään yhtyettä ja etsiä keikkoja soitettavaksi.
  
##### Välipalautus 2 ominaisuudet:

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen
- Käyttäjä näkee etusivulla listan keikoista (sisältää yhtyeen nimen, keikan päivämäärän, sijainnin, kuvauksen ja eri soittajien tarpeen)
- Käyttäjä voi lisätä itselleen yhtyeen ja ilmoittaa yhtyeelleen keikkoja johon tarvitaan soittajia
- Käyttäjä pystyy ilmoittautumaan itsensä keikalle tuuraajaksi

## Alustava relaatiokaavio

![alt text](https://github.com/Faktatykki/musician-reserve-service/blob/main/documentation/musician-reserve-schema.png)

## Huomioita arvioijalle

Sovellus on vielä toistaiseksi hyvin primitiivisessä vaiheessa, mutta raamit ovat kasassa tarvittavalle toiminnallisuudelle.
Koodin hajauttaminen eri moduuleihin ei ole lähimaillakaan riittävää vielä. Sovelluslogiikka ja muu toiminnallisuus on toistaiseksi
hyvinkin sekaisin kirjoitettua. Kommentit auttavat selvittämään, että miten hajauttaminen tullaan toteuttamaan.

"premature optimization is the root of all evil." - Sir Tony Hoare

## Testaaminen 

Sovellusta voi testata Herokussa osoitteessa:

[Musician-reserve-service](https://musician-reserve-service.herokuapp.com/)

Tietokannasta löytyy tällä hetkellä kaksi käyttäjää:

Testi
Testi2

Salasanat ovat samat kuin käyttäjänimet. Kehotan kumminkin luomaan kaksi uutta käyttäjää jotta testata ilmoittautumis-toiminnallisuutta keikalle,
sillä ilmoitetut keikat näkyvät toistaiseksi vain toisille käyttäjille.

Rattoisia testaamisia!









