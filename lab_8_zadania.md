# Lab 8 - Zadania GraphQL

## Zadanie 2 - Dodatkowe resolvery

### 1. Filtrowanie postów po fragmencie tytułu
```graphql
query {
  postsByTitleFragment(substr: "Django") {
    id
    title
    text
  }
}
```

### 2. Liczba postów użytkownika
```graphql
query {
  postCountByUser(userId: 1)
}
```

### 3. Tematy dla kategorii zawierającej frazę
```graphql
query {
  topicsByCategoryNameFragment(substr: "Prog") {
    id
    title
    category {
      name
    }
  }
}
```

## Zadanie 3 - Mutacje dla Post

### 1. Tworzenie posta
```graphql
mutation {
  createPost(
    title: "Nowy Post GraphQL", 
    text: "Treść posta stworzonego przez GraphQL", 
    slug: "nowy-post-graphql", 
    topicId: 1, 
    createdById: 1
  ) {
    post {
      id
      title
      createdBy {
        username
      }
    }
  }
}
```

### 2. Aktualizacja posta
```graphql
mutation {
  updatePost(id: 4, title: "Zaktualizowany Tytuł GraphQL") {
    post {
      id
      title
      text
    }
  }
}
```

### 3. Usuwanie posta
```graphql
mutation {
  deletePost(id: 4) {
    success
  }
}
```

## Podstawowe zapytania (z labu)

### Wszystkie kategorie
```graphql
query {
  allCategories {
    id
    name
  }
}
```

### Post po ID
```graphql
query {
  postById(id: 1) {
    title
    text
    topic {
      title
    }
  }
}
```
