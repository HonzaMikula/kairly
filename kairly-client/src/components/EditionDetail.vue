<template>
  <edition-detail-view>
    
    <div>
      <edition-detail--header>
        <h1>Malostranské noviny</h1>
      </edition-detail--header>

      <edition-detail--description>
        <p>
          Přehled toho nejzajímavějšího, co přinesla česká politika. Výběr nejlepších článků, komentářů a tweetů mapující aktuální situaci na politické scéně.
        </p>
        
        <div>
          <div>
            <h3>Periodicity</h3>
            <p>Daily</p>
          </div>

          <div>
            <h3>Issues</h3>
            <p>45</p>
          </div>

          <div>
            <h3>Subscribers</h3>
            <p>23</p>
          </div>
        </div>
      </edition-detail--description>

      <edition-detail--subscribe>
        <button>Subscribe Edition</button>
        <p>10 CZK per month</p>
      </edition-detail--subscribe>
      
      <edition-detail--picture>
        <img src="http://kairly.com/media/editions/malostranskenoviny.jpg" alt="Malostranské noviny"/>
      </edition-detail--picture>
    </div>


    <edition-detail--last-edition>
      <h2><span>Check the Last Issue</span></h2>

      <p>Here will be last edition without access to detail of the articles</p>
    </edition-detail--last-edition>
  </edition-detail-view>
</template>


<script>
export default {
  name: 'EditionDetail'
}
</script>