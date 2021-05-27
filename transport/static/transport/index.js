// Download 10 offers at a time
// Start from first offer
let counter = 1;

// Download 10 offers
const quantity = 10;

var max_offers = quantity + 2

var order = 'timestamp.True'

class Offers extends React.Component {
    render() {
        const offers = this.props.data.offers;
        const offeritems = offers.map((offer) =>
        <div className="col" key={offer.id} style={{ marginBottom: '28px' }}>
            <div className="card mb-2 rounded-6 shadow p-2" style={{ minHeight: '300px', minWidth: '300px', maxWidth: '475px', borderRadius: '15px', paddingRight: '0%', margin: '0%' }}>
                <div className="card-body" style={{ padding: '15px' }}>
                    <div className="row">
                        <div className='col' style={{ textAlign: 'left', minWidth: '270px', maxWidth: '400px' }}>
                            <img src={offer.photo} alt="image"  style={{ maxWidth: '100%', minWidth: 'none', borderRadius: '10px' }} />
                            <a href={offer.details} ><button type="button" className="btn btn-warning" style={{ width: '100%', color: 'white', marginTop: '6%' }}><b>DETAILS</b></button></a>
                        </div>
                        <div className='col' style={{ textAlign: 'left', minWidth: '150px', marginTop: '5px', marginBottom: '0px'}} >
                            <h4 style={{ color: '#2a9d8f' }}>{offer.name}</h4>
                            <br/>
                            <div name="icons_gread" style={{ maxWidth: '200px' }}>
                                <div className="row">
                                    <div className="col" style={{ marginTop: '7px', maxWidth: '70px' }}><img src='/static/transport/icons/icon_man.svg' style={{ width: '17px', verticalAlign: '-10%', marginRight: '5px' }} />{offer.passenger_places}</div>
                                    <div className="col" style={{ marginTop: '7px' }}><img src='/static/transport/icons/icon_conditioner.svg' style={{ width: '17px', verticalAlign: '-15%', marginRight: '5px' }} />A/C {offer.air_conditioner}</div>
                                </div>
                                <div className="row">
                                    <div className="col" style={{ marginTop: '7px', maxWidth: '70px' }}><img src='/static/transport/icons/icon_bagage.svg' style={{ width: '17px', verticalAlign: '-10%', marginRight: '5px' }} />{offer.baggage_places}</div>
                                    <div className="col" style={{ marginTop: '7px' }}><img src='/static/transport/icons/icon_gearbox.svg' style={{ width: '17px', verticalAlign: '-10%', marginRight: '5px' }} />{offer.automat_gearbox}</div>
                                </div>
                                <div style={{ marginTop: '10px', fontSize: '17px' }}><img src='/static/transport/icons/icon_star.svg' style={{ width: '18px', verticalAlign: '-11%', marginRight: '5px' }} />{offer.owner_rating}/<span style={{ fontSize: '11.5px' }}>5</span> <a href={offer.owner_page} className="btn btn-link" style={{ fontSize: '15px', color: 'black', padding: '0%', paddingBottom: '3px', textDecoration: 'underline' }}>{offer.responses_count} reviews</a></div>
                            </div>
                            <div style={{ marginTop: '33%', fontSize: '16px' }} >
                                <span style={{ marginBottom: '0%', fontSize: '22px', color: '#2a9d8f' }} ><b>${offer.price_per_day}</b></span> per day
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        );
        return (
            <div className="row row-cols-1 row-cols-md-2 mb-2 text-center" >{offeritems}</div>
        );
    }
}

// Loads next set of offers
function load(order) {

    // Set start and end offers numbers, and update counter
    const start = counter;
    const end = start + quantity - 1;
    counter = end + 1;
    
    if (max_offers > end || end === quantity) {
        // Get new posts and add posts
        fetch(`/offers?start=${start}&end=${end}&order=${order}`)
        .then(response => response.json())
        .then(data => {
            max_offers = data.max;
            var element_id = `#offers-${start}`
            ReactDOM.render(<Offers data={data} />, document.querySelector(element_id)); 
        });
        var new_element = document.createElement('div');
        new_element.id = `offers-${counter}`;
        document.querySelector('#offers').appendChild(new_element);
    }
    
}

// When DOM loads, render 10 first offers
document.addEventListener('DOMContentLoaded', load(order));

// When scrolled to bottom, load more 10 offers
window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        load(order);
    }
}

document.addEventListener("click", event => {
    //alert(event.target.value)
    if (event.target.id === 'sort') {
        order = event.target.value;
        counter = 1;
        max_offers = quantity + 2;
        document.querySelector('#offers').innerHTML = "";
        var new_element = document.createElement('div');
        new_element.id = `offers-${counter}`;
        document.querySelector('#offers').appendChild(new_element);
        load(order);
    }
});