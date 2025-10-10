from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Kraj(models.Model):
    """Model reprezentujący kraj docelowy."""
    nazwa = models.CharField(max_length=100, unique=True)
    kod = models.CharField(max_length=3, unique=True, help_text="Kod ISO kraju (np. PL, FR)")
    kontynent = models.CharField(max_length=50)
    opis = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Kraj"
        verbose_name_plural = "Kraje"
        ordering = ['nazwa']
    
    def __str__(self):
        return self.nazwa


class LiniaLotnicza(models.Model):
    """Model reprezentujący linię lotniczą."""
    nazwa = models.CharField(max_length=100)
    kod_iata = models.CharField(max_length=3, unique=True, help_text="Kod IATA (np. LOT, LH)")
    kraj_pochodzenia = models.ForeignKey(Kraj, on_delete=models.SET_NULL, null=True, related_name='linie_lotnicze')
    strona_www = models.URLField(blank=True)
    
    class Meta:
        verbose_name = "Linia lotnicza"
        verbose_name_plural = "Linie lotnicze"
        ordering = ['nazwa']
    
    def __str__(self):
        return f"{self.nazwa} ({self.kod_iata})"


class Lot(models.Model):
    """Model reprezentujący lot."""
    numer_lotu = models.CharField(max_length=10, unique=True)
    linia_lotnicza = models.ForeignKey(LiniaLotnicza, on_delete=models.CASCADE, related_name='loty')
    lotnisko_wylotu = models.CharField(max_length=100)
    lotnisko_przylotu = models.CharField(max_length=100)
    data_wylotu = models.DateTimeField()
    data_przylotu = models.DateTimeField()
    czas_trwania = models.DurationField(help_text="Czas trwania lotu")
    
    class Meta:
        verbose_name = "Lot"
        verbose_name_plural = "Loty"
        ordering = ['data_wylotu']
    
    def __str__(self):
        return f"{self.numer_lotu} - {self.lotnisko_wylotu} → {self.lotnisko_przylotu}"


class Hotel(models.Model):
    """Model reprezentujący hotel."""
    KATEGORIE_GWIAZDKI = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]
    
    nazwa = models.CharField(max_length=200)
    kraj = models.ForeignKey(Kraj, on_delete=models.CASCADE, related_name='hotele')
    miasto = models.CharField(max_length=100)
    adres = models.CharField(max_length=200)
    kategoria = models.IntegerField(choices=KATEGORIE_GWIAZDKI, validators=[MinValueValidator(1), MaxValueValidator(5)])
    opis = models.TextField()
    udogodnienia = models.TextField(help_text="Udogodnienia w hotelu (basen, siłownia, spa, etc.)")
    strona_www = models.URLField(blank=True)
    
    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hotele"
        ordering = ['nazwa']
    
    def __str__(self):
        return f"{self.nazwa} ({self.kategoria}⭐) - {self.miasto}, {self.kraj}"


class Wycieczka(models.Model):
    """Model reprezentujący wycieczkę."""
    OPCJE_CENOWE = [
        ('STANDARD', 'Standard'),
        ('PREMIUM', 'Premium'),
        ('LUXURY', 'Luxury'),
    ]
    
    nazwa = models.CharField(max_length=200)
    opis = models.TextField()
    kraj_docelowy = models.ForeignKey(Kraj, on_delete=models.CASCADE, related_name='wycieczki')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='wycieczki')
    lot_tam = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='wycieczki_tam', verbose_name="Lot w jedną stronę")
    lot_powrot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='wycieczki_powrot', null=True, blank=True, verbose_name="Lot powrotny")
    
    # Okres trwania - pola bezpośrednio w modelu (lepsze rozwiązanie niż osobny model)
    data_rozpoczecia = models.DateField()
    data_zakonczenia = models.DateField()
    liczba_dni = models.IntegerField(validators=[MinValueValidator(1)])
    liczba_nocy = models.IntegerField(validators=[MinValueValidator(0)])
    
    # Ceny
    opcja_cenowa = models.CharField(max_length=20, choices=OPCJE_CENOWE, default='STANDARD')
    cena_za_osobe = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cena_dziecko = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    
    # Dodatowe informacje
    max_liczba_osob = models.IntegerField(validators=[MinValueValidator(1)])
    aktywna = models.BooleanField(default=True, help_text="Czy wycieczka jest aktualnie dostępna")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Wycieczka"
        verbose_name_plural = "Wycieczki"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.nazwa} - {self.kraj_docelowy} ({self.data_rozpoczecia})"
    
    @property
    def srednia_ocena(self):
        """Oblicza średnią ocenę z opinii."""
        opinie = self.opinie.all()
        if opinie:
            return sum(o.ocena for o in opinie) / len(opinie)
        return None


class Klient(models.Model):
    """Model reprezentujący klienta biura podróży."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='profil_klienta')
    imie = models.CharField(max_length=100)
    nazwisko = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefon = models.CharField(max_length=20)
    adres = models.CharField(max_length=200, blank=True)
    kod_pocztowy = models.CharField(max_length=10, blank=True)
    miasto = models.CharField(max_length=100, blank=True)
    kraj = models.ForeignKey(Kraj, on_delete=models.SET_NULL, null=True, blank=True, related_name='klienci')
    
    data_rejestracji = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Klient"
        verbose_name_plural = "Klienci"
        ordering = ['nazwisko', 'imie']
    
    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.email})"


class Rezerwacja(models.Model):
    """Model reprezentujący rezerwację wycieczki."""
    STATUS_CHOICES = [
        ('OCZEKUJACA', 'Oczekująca'),
        ('POTWIERDZONA', 'Potwierdzona'),
        ('OPLACONA', 'Opłacona'),
        ('ANULOWANA', 'Anulowana'),
        ('ZAKONCZONA', 'Zakończona'),
    ]
    
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE, related_name='rezerwacje')
    wycieczka = models.ForeignKey(Wycieczka, on_delete=models.CASCADE, related_name='rezerwacje')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OCZEKUJACA')
    
    liczba_doroslich = models.IntegerField(validators=[MinValueValidator(1)])
    liczba_dzieci = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    
    # Ceny
    cena_calkowita = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    zaliczka = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    pozostalo_do_zaplaty = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Daty
    data_rezerwacji = models.DateTimeField(auto_now_add=True)
    data_potwierdzenia = models.DateTimeField(null=True, blank=True)
    data_oplaty = models.DateTimeField(null=True, blank=True)
    
    uwagi = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Rezerwacja"
        verbose_name_plural = "Rezerwacje"
        ordering = ['-data_rezerwacji']
    
    def __str__(self):
        return f"Rezerwacja #{self.id} - {self.klient} → {self.wycieczka.nazwa} ({self.status})"
    
    def save(self, *args, **kwargs):
        """Automatyczne obliczenie pozostałej kwoty do zapłaty."""
        self.pozostalo_do_zaplaty = self.cena_calkowita - self.zaliczka
        super().save(*args, **kwargs)


class Opinia(models.Model):
    """Model reprezentujący opinię o wycieczce."""
    wycieczka = models.ForeignKey(Wycieczka, on_delete=models.CASCADE, related_name='opinie')
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE, related_name='opinie')
    rezerwacja = models.OneToOneField(Rezerwacja, on_delete=models.CASCADE, null=True, blank=True, related_name='opinia')
    
    # System ocen 1-5
    ocena = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Ocena od 1 do 5 gwiazdek"
    )
    tytul = models.CharField(max_length=200)
    tresc = models.TextField()
    
    # Szczegółowe oceny
    ocena_hotelu = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    ocena_lotu = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    ocena_obslugi = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    
    data_dodania = models.DateTimeField(auto_now_add=True)
    zweryfikowana = models.BooleanField(default=False, help_text="Czy opinia została zweryfikowana przez administratora")
    
    class Meta:
        verbose_name = "Opinia"
        verbose_name_plural = "Opinie"
        ordering = ['-data_dodania']
        # Jeden klient może dodać tylko jedną opinię do danej wycieczki
        unique_together = ['wycieczka', 'klient']
    
    def __str__(self):
        gwiazdki = "⭐" * self.ocena
        return f"{gwiazdki} - {self.tytul} (od {self.klient})"
