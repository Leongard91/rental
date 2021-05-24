// Download 10 offers at a time
// Start from first offer
let counter = 1;

// Download 10 offers
const quantity = 10;

class Offers extends React.Component {
    render() {
        const offers = this.props.data.offers;
        const offeritems = offers.map((offer) =>
        <div className="col" key={offer.id}>
            <div className="card mb-2 rounded-6 shadow p-2" style={{ minHeight: '300px', marginTop: '20px', minWidth: '300px' }}>
                <div className="card-body">
                    <div className="row">
                        <div className='col' style={{ textAlign: 'left', color: '#2798F8', minWidth: '250px', marginBottom: '20px' }}>
                            <h4>{offer.name}</h4>
                            <h5>Price: {offer.price_per_day} USD / day</h5>
                            <div className="lh-sm">{offer.description}</div>
                            <div className="align-bottom" style={{ color: 'grey', fontSize: '15px' }}>Created in {offer.timestamp}</div>
                        </div>
                        <div className='col' style={{ textAlign: 'center' }}>
                            <img src={offer.photo} alt="image" className="rounded float-start " style={{ width: '250px' }} />
                        </div>
                    </div>
                </div>
                <div className="row align-bottom" style={{ textAlign: 'left', margin: '10px'}}>
                    <div className="col" style={{ color: '#2798F8' }}><img src='https://raw.githubusercontent.com/Leongard91/rental/main/transport/static/transport/pointer.png' style={{ width: '23px', verticalAlign: '-20%', marginRight: '0px'}} />{offer.pick_up_location}</div> 
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

// When DOM loads, render 10 first offers
document.addEventListener('DOMContentLoaded', load());

// When scrolled to bottom, load more 10 offers
window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        load();
    }
}
