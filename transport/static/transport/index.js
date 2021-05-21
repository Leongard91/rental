// Download 10 offers at a time
// Start from first offer
let counter = 1;

// Download 10 offers
const quantity = 2;

// When DOM loads, render 10 first offers
document.addEventListener('DOMContentLoaded', load());

// When scrolled to bottom, load more 10 offers
window.onscroll = () => {
    if (window.innerHeight + window.scrolY >= document.body.offsetHeight) {
        load();
    }
}

class Offers extends React.Component {
    render() {
        const offers = this.props.data.offers;
        const offeritems = offers.map((offer) =>
        <div className="row" key={offer.id}>
            <div className='col' style={{ textAlign: 'center' }}>
                <img src={offer.photo} alt="image" className="rounded float-start" style={{ maxHeight: '300px' }} />
            </div>
            <div className='col'>
                <h4>{offer.name}</h4>
                <h5>Price: {offer.price_per_day} USD / day</h5>
                <div className="lh-sm">{offer.description}</div>
                <div style={{ color: 'grey' }}>Created {offer.timestamp}</div>
            </div>
        </div>
        );
        return (
            <div>{offeritems}</div>
        );
    }
}

// Loads next set of offers
function load() {

    // Set start and end offers numbers, and update counter
    const start = counter;
    const end = start + quantity - 1;
    counter = end + 1;

    
    // Get new posts and add posts
    fetch(`/offers?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data => {
        ReactDOM.render(<Offers data={data} />, document.querySelector('#offers'));
    });
}

