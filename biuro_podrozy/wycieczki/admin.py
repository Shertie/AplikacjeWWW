from django.contrib import admin
from django.utils.html import format_html
from .models import Kraj, LiniaLotnicza, Lot, Hotel, Wycieczka, Klient, Rezerwacja, Opinia


@admin.register(Kraj)
class KrajAdmin(admin.ModelAdmin):
    """Panel administracyjny dla modelu Kraj."""
    list_display = ['nazwa', 'kod', 'kontynent', 'liczba_hoteli', 'liczba_wycieczek']
    list_filter = ['kontynent']
    search_fields = ['nazwa', 'kod']
    ordering = ['nazwa']
    
    def liczba_hoteli(self, obj):
        return obj.hotele.count()
    liczba_hoteli.short_description = 'Liczba hoteli'
    
    def liczba_wycieczek(self, obj):
        return obj.wycieczki.count()
    liczba_wycieczek.short_description = 'Liczba wycieczek'


@admin.register(LiniaLotnicza)
class LiniaLotniczaAdmin(admin.ModelAdmin):
    """Panel administracyjny dla modelu Linia Lotnicza."""
    list_display = ['nazwa', 'kod_iata', 'kraj_pochodzenia', 'liczba_lotow', 'link_www']
    list_filter = ['kraj_pochodzenia']
    search_fields = ['nazwa', 'kod_iata']
    ordering = ['nazwa']
    
    def liczba_lotow(self, obj):
        return obj.loty.count()
    liczba_lotow.short_description = 'Liczba lotów'
    
    def link_www(self, obj):
        if obj.strona_www:
            return format_html('<a href="{}" target="_blank">🌐 Strona WWW</a>', obj.strona_www)
        return '-'
    link_www.short_description = 'Strona'


@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    """Panel administracyjny dla modelu Lot."""
    list_display = ['numer_lotu', 'linia_lotnicza', 'trasa', 'data_wylotu', 'data_przylotu', 'czas_trwania']
    list_filter = ['linia_lotnicza', 'data_wylotu']
    search_fields = ['numer_lotu', 'lotnisko_wylotu', 'lotnisko_przylotu']
    date_hierarchy = 'data_wylotu'
    ordering = ['-data_wylotu']
    
    def trasa(self, obj):
        return f"{obj.lotnisko_wylotu} → {obj.lotnisko_przylotu}"
    trasa.short_description = 'Trasa'


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    """Panel administracyjny dla modelu Hotel."""
    list_display = ['nazwa', 'miasto', 'kraj', 'kategoria_gwiazdki', 'liczba_wycieczek', 'link_www']
    list_filter = ['kategoria', 'kraj', 'miasto']
    search_fields = ['nazwa', 'miasto', 'adres']
    ordering = ['nazwa']
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('nazwa', 'kraj', 'miasto', 'adres', 'kategoria')
        }),
        ('Opis i udogodnienia', {
            'fields': ('opis', 'udogodnienia', 'strona_www')
        }),
    )
    
    def kategoria_gwiazdki(self, obj):
        return "⭐" * obj.kategoria
    kategoria_gwiazdki.short_description = 'Kategoria'
    
    def liczba_wycieczek(self, obj):
        return obj.wycieczki.count()
    liczba_wycieczek.short_description = 'Liczba wycieczek'
    
    def link_www(self, obj):
        if obj.strona_www:
            return format_html('<a href="{}" target="_blank">🌐 Strona</a>', obj.strona_www)
        return '-'
    link_www.short_description = 'WWW'


class OpiniaInline(admin.TabularInline):
    """Inline dla opinii w panelu wycieczek."""
    model = Opinia
    extra = 0
    readonly_fields = ['klient', 'ocena', 'data_dodania']
    fields = ['klient', 'ocena', 'tytul', 'zweryfikowana']


class RezerwacjaInline(admin.TabularInline):
    """Inline dla rezerwacji w panelu wycieczek."""
    model = Rezerwacja
    extra = 0
    readonly_fields = ['klient', 'status', 'data_rezerwacji', 'cena_calkowita']
    fields = ['klient', 'status', 'liczba_doroslich', 'liczba_dzieci', 'cena_calkowita']


@admin.register(Wycieczka)
class WycieczkaAdmin(admin.ModelAdmin):
    """Panel administracyjny dla modelu Wycieczka."""
    list_display = ['nazwa', 'kraj_docelowy', 'hotel', 'okres', 'cena_display', 'opcja_cenowa', 
                    'srednia_ocena_display', 'liczba_rezerwacji', 'status_aktywna']
    list_filter = ['aktywna', 'opcja_cenowa', 'kraj_docelowy', 'data_rozpoczecia']
    search_fields = ['nazwa', 'opis']
    date_hierarchy = 'data_rozpoczecia'
    ordering = ['-data_rozpoczecia']
    inlines = [RezerwacjaInline, OpiniaInline]
    
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('nazwa', 'opis', 'kraj_docelowy', 'hotel', 'aktywna')
        }),
        ('Loty', {
            'fields': ('lot_tam', 'lot_powrot')
        }),
        ('Terminy', {
            'fields': ('data_rozpoczecia', 'data_zakonczenia', 'liczba_dni', 'liczba_nocy')
        }),
        ('Ceny i dostępność', {
            'fields': ('opcja_cenowa', 'cena_za_osobe', 'cena_dziecko', 'max_liczba_osob')
        }),
    )
    
    def okres(self, obj):
        return f"{obj.data_rozpoczecia} - {obj.data_zakonczenia} ({obj.liczba_dni}d/{obj.liczba_nocy}n)"
    okres.short_description = 'Okres'
    
    def cena_display(self, obj):
        return f"{obj.cena_za_osobe} PLN"
    cena_display.short_description = 'Cena/os'
    
    def srednia_ocena_display(self, obj):
        srednia = obj.srednia_ocena
        if srednia:
            gwiazdki = "⭐" * int(round(srednia))
            return f"{gwiazdki} ({srednia:.1f})"
        return "Brak ocen"
    srednia_ocena_display.short_description = 'Średnia ocena'
    
    def liczba_rezerwacji(self, obj):
        return obj.rezerwacje.count()
    liczba_rezerwacji.short_description = 'Rezerwacje'
    
    def status_aktywna(self, obj):
        if obj.aktywna:
            return format_html('<span style="color: green;">✓ Aktywna</span>')
        return format_html('<span style="color: red;">✗ Nieaktywna</span>')
    status_aktywna.short_description = 'Status'


@admin.register(Klient)
class KlientAdmin(admin.ModelAdmin):
    """Panel administracyjny dla modelu Klient."""
    list_display = ['pelne_imie', 'email', 'telefon', 'miasto', 'kraj', 'liczba_rezerwacji', 'data_rejestracji']
    list_filter = ['kraj', 'data_rejestracji']
    search_fields = ['imie', 'nazwisko', 'email', 'telefon']
    date_hierarchy = 'data_rejestracji'
    ordering = ['-data_rejestracji']
    
    fieldsets = (
        ('Dane osobowe', {
            'fields': ('user', 'imie', 'nazwisko', 'email', 'telefon')
        }),
        ('Adres', {
            'fields': ('adres', 'kod_pocztowy', 'miasto', 'kraj')
        }),
    )
    
    def pelne_imie(self, obj):
        return f"{obj.imie} {obj.nazwisko}"
    pelne_imie.short_description = 'Imię i nazwisko'
    
    def liczba_rezerwacji(self, obj):
        count = obj.rezerwacje.count()
        if count > 0:
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', count)
        return count
    liczba_rezerwacji.short_description = 'Rezerwacje'


@admin.register(Rezerwacja)
class RezerwacjaAdmin(admin.ModelAdmin):
    """Panel administracyjny dla modelu Rezerwacja."""
    list_display = ['id', 'klient', 'wycieczka_skrot', 'status_colored', 'liczba_osob_display', 
                    'cena_calkowita', 'pozostalo_display', 'data_rezerwacji']
    list_filter = ['status', 'data_rezerwacji', 'wycieczka__kraj_docelowy']
    search_fields = ['klient__imie', 'klient__nazwisko', 'klient__email', 'wycieczka__nazwa']
    date_hierarchy = 'data_rezerwacji'
    ordering = ['-data_rezerwacji']
    readonly_fields = ['pozostalo_do_zaplaty', 'data_rezerwacji']
    
    fieldsets = (
        ('Informacje podstawowe', {
            'fields': ('klient', 'wycieczka', 'status')
        }),
        ('Uczestnicy', {
            'fields': ('liczba_doroslich', 'liczba_dzieci')
        }),
        ('Finanse', {
            'fields': ('cena_calkowita', 'zaliczka', 'pozostalo_do_zaplaty')
        }),
        ('Daty i terminy', {
            'fields': ('data_rezerwacji', 'data_potwierdzenia', 'data_oplaty')
        }),
        ('Dodatkowe', {
            'fields': ('uwagi',),
            'classes': ('collapse',)
        }),
    )
    
    def wycieczka_skrot(self, obj):
        return f"{obj.wycieczka.nazwa[:30]}..."
    wycieczka_skrot.short_description = 'Wycieczka'
    
    def status_colored(self, obj):
        colors = {
            'OCZEKUJACA': 'orange',
            'POTWIERDZONA': 'blue',
            'OPLACONA': 'green',
            'ANULOWANA': 'red',
            'ZAKONCZONA': 'gray',
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = 'Status'
    
    def liczba_osob_display(self, obj):
        total = obj.liczba_doroslich + obj.liczba_dzieci
        return f"{total} ({obj.liczba_doroslich}d + {obj.liczba_dzieci}dz)"
    liczba_osob_display.short_description = 'Liczba osób'
    
    def pozostalo_display(self, obj):
        if obj.pozostalo_do_zaplaty > 0:
            return format_html(
                '<span style="color: red; font-weight: bold;">{} PLN</span>',
                obj.pozostalo_do_zaplaty
            )
        return format_html('<span style="color: green;">✓ Opłacone</span>')
    pozostalo_display.short_description = 'Pozostało'


@admin.register(Opinia)
class OpiniaAdmin(admin.ModelAdmin):
    """Panel administracyjny dla modelu Opinia."""
    list_display = ['tytul_skrot', 'klient', 'wycieczka_skrot', 'ocena_gwiazdki', 
                    'szczegolowe_oceny', 'data_dodania', 'status_weryfikacji']
    list_filter = ['ocena', 'zweryfikowana', 'data_dodania', 'wycieczka__kraj_docelowy']
    search_fields = ['tytul', 'tresc', 'klient__imie', 'klient__nazwisko']
    date_hierarchy = 'data_dodania'
    ordering = ['-data_dodania']
    readonly_fields = ['data_dodania']
    
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('wycieczka', 'klient', 'rezerwacja')
        }),
        ('Ocena', {
            'fields': ('ocena', 'tytul', 'tresc')
        }),
        ('Szczegółowe oceny', {
            'fields': ('ocena_hotelu', 'ocena_lotu', 'ocena_obslugi'),
            'classes': ('collapse',)
        }),
        ('Weryfikacja', {
            'fields': ('zweryfikowana', 'data_dodania')
        }),
    )
    
    def tytul_skrot(self, obj):
        return obj.tytul[:50] + "..." if len(obj.tytul) > 50 else obj.tytul
    tytul_skrot.short_description = 'Tytuł'
    
    def wycieczka_skrot(self, obj):
        return f"{obj.wycieczka.nazwa[:30]}..."
    wycieczka_skrot.short_description = 'Wycieczka'
    
    def ocena_gwiazdki(self, obj):
        return "⭐" * obj.ocena
    ocena_gwiazdki.short_description = 'Ocena'
    
    def szczegolowe_oceny(self, obj):
        parts = []
        if obj.ocena_hotelu:
            parts.append(f"🏨 {obj.ocena_hotelu}")
        if obj.ocena_lotu:
            parts.append(f"✈️ {obj.ocena_lotu}")
        if obj.ocena_obslugi:
            parts.append(f"👤 {obj.ocena_obslugi}")
        return " | ".join(parts) if parts else "-"
    szczegolowe_oceny.short_description = 'Szczegóły'
    
    def status_weryfikacji(self, obj):
        if obj.zweryfikowana:
            return format_html('<span style="color: green;">✓ Zweryfikowana</span>')
        return format_html('<span style="color: orange;">⏳ Oczekuje</span>')
    status_weryfikacji.short_description = 'Weryfikacja'


# Konfiguracja nagłówka panelu administracyjnego
admin.site.site_header = "Biuro Podróży - Panel Administracyjny"
admin.site.site_title = "Biuro Podróży Admin"
admin.site.index_title = "Zarządzanie systemem rezerwacji"
