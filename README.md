# Varahenkilöpalvelu muusikoille


Sovellus on tarkoitettu muusikoille jotka etsivät yksittäisille keikoille soittajia/tuuraajia esiintymään tai keikkoja soittaakseen. Sovelluksessa käyttäjä voi rekisteröidä yhtyeensä (ja määritellä tarpeen eri instrumenttien soittajille) ja yhtyeelle keikkoja, johon eri käyttäjät voivat ilmoittautua tuuraamaan. Käyttäjä voi rekisteröityä palveluun myös luomatta yhtäkään yhtyettä ja etsiä vain keikkoja soitettavaksi.
  
##### Ominaisuudet:

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen
- Käyttäjä näkee etusivulla listan keikoista (sisältää yhtyeen nimen, keikan päivämäärän, sijainnin, kuvauksen ja eri soittajien tarpeen)
- Käyttäjä näkee eri näkymissä keikat mihin itse on ilmoittautunut soittamaan ja keikat jotka on itse ilmoittanut, sekä niihin ilmoittautuneet muut soittajat
- Käyttäjä voi lisätä itselleen yhtyeen ja ilmoittaa yhtyeelleen keikkoja johon tarvitaan soittajia
- Käyttäjä pystyy ilmoittautumaan itsensä keikalle tuuraajaksi
- Käyttäjä pystyy poistamaan omia yhtyeitään, keikkojaan ja ilmoittautumisiaan
- Käyttäjä näkee etusivulla pientä statistiikkaa liittyen keikkoihin ja yhtyeisiin

## Relaatiokaavio

![alt text](https://github.com/Faktatykki/musician-reserve-service/blob/main/documentation/musician-reserve-schema.png)

## Testaaminen 

Sovellusta voi testata Herokussa seuraamalla seuraavaa linkkiä:

[Musician-reserve-service](https://musician-reserve-service.herokuapp.com/)

Tietokannasta löytyy tällä hetkellä kaksi käyttäjää:

Käyttäjänimi: Testi1  
Salasana: Testaaja1 
  
Käyttäjänimi: Testi2  
Salasana: Testaaja2  
  
  
Käyttäjä "Testi1" on luonut yhtyeen ja ilmoittanut yhtyeelle kolme keikkaa. Käyttäjällä "Testi2" pystyy testaamaan keikoille ilmoittautumista ja tähän 
liittyviä toiminnallisuuksia. Parhaimman kuvan sovelluksesta saa aloittamalla "prosessin" alusta asti, eli luomalla uuden käyttäjän ja yhtyeen jne.. 

Olen nyt hetken venkslannut sovelluksen parissa, joten on hyvin mahdollista, että vauhtisokeus on iskenyt. Tästä huolimatta minusta tuntuu, että käyttöliittymä 
on verrattain intuitiivinen, enkä aio liikaa ohjeistaa tässä käyttäjän toimintaa.

  
Rattoisia testaamisia!









