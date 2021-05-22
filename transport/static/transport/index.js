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
        <div className="col" key={offer.id}>
            <div className="card mb-2 rounded-6 shadow p-2" style={{ minHeight: '300px', marginTop: '20px', minWidth: '300px' }}>
                <div className="card-body">
                    <div className="row">
                        <div className='col' style={{ textAlign: 'left', color: '#2798F8' }}>
                            <h4>{offer.name}</h4>
                            <h5>Price: {offer.price_per_day} USD / day</h5>
                            <div className="lh-sm">{offer.description}</div>
                            <div style={{ color: 'grey' }}>Created in {offer.timestamp}</div>
                        </div>
                        <div className='col' style={{ textAlign: 'center' }}>
                            <img src={offer.photo} alt="image" className="rounded float-start " style={{ width: '250px' }} />
                        </div>
                    </div>
                </div>
                <div className="row align-bottom" style={{ textAlign: 'left', margin: '10px'}}>
                    <div className="col"><img src='https://cdn0.iconfinder.com/data/icons/navigation-easy/64/geolocation-map-pointer-gps-512.png' style={{ width: '23px', verticalAlign: '-25%'}} />{offer.pick_up_location}</div> 
                    <div className="col" style={{ textAlign: 'right' }}><button type="button" className="btn btn-warning" style={{ width: '125px', color: 'white' }}><b>RENT</b></button></div>
                </div>
            </div>
        </div>

        );
        return (
            <div className="row row-cols-1 row-cols-md-2 mb-2 text-center">{offeritems}</div>
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

