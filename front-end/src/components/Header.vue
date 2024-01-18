<template>
  <header id="title-wrapper">
    <h1>Dragons MTG Card Collection System</h1>
    <img
        src="/mtg_logo.png"
        alt="MTG Logo"
    >
    <nav>
      <router-link to="/collection">Collection</router-link>
      <router-link to="/decks">Decks</router-link>
      <router-link to="/search">Search</router-link>
    </nav>
  </header>
</template>

<style scoped lang="scss">
#title-wrapper {
  display: flex;
  margin: 1rem 2rem;
  align-items: center;

  h1 {
    margin: 0;
  }
  img {
    height: 3em;
  }
  nav {
    margin-left: auto;
    display: flex;
    gap: 1rem;
  }
}
</style>
