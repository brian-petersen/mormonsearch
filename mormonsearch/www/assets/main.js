import Vue from './vendor/vue.js'

new Vue({
    el: '#app',
    data: {
        query: '',
        lastQuery: '',
        hasSearched: false,
        verses: [
            // A few verses are included for easier local development (mainly with styles)
            // { reference: "1 Corinthians 13:4", text: "Charity suffereth long, and is kind; charity envieth not; charity vaunteth not itself, is not puffed up," },
            // { reference: "1 Corinthians 13:13", text: "And now abideth faith, hope, charity, these three; but the greatest of these is charity." }
        ],
        verseSearchCount: 0
    },
    computed: {
        csvUrl: function() {
            return `/api/search?query=${this.lastQuery}&limit=${this.verseSearchCount}&format=csv`
        }
    },
    methods: {
        onSubmit: function () {
            if (this.query) {
                this.hasSearched = true
                this.lastQuery = this.query
                this.performSearch(this.query)
            } else {
                this.resetResults()
            }
        },
        onShowAll: function() {
            this.performSearch(this.lastQuery, this.verseSearchCount)
        },
        performSearch: function (query, count=10) {
            fetch(`/api/search?query=${query}&limit=${count}`)
            .then(res => res.json())
            .then(({ verses, totalCount }) => {
                this.verses = verses
                this.verseSearchCount = totalCount
            })
        },
        resetResults: function () {
            this.verses = []
        }
    }
})
