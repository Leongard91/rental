// Search page filters
const filters = [];
$(document).ready(
    $(document).click(event => {
        if (event.target.type === 'checkbox'){
            $('#new_search').hide();

            // Add filters to the list
            if (filters.includes(event.target.value)) {
                let index = filters.indexOf(event.target.value);
                filters.splice(index, 1);
            } else {
                filters.push(event.target.value);
            }
             
            // Download filtered offers
            load();
        }
    }),

    $('#order').change(event => {
        load(event.target.value);
    })
)

function load(sort_value) {

    // Get new posts and add posts
    fetch(`/filter?filters=${filters}&order=${sort_value}`)
    .then(response => response.json())
    .then(data => {
        ReactDOM.render(<Offers data={data} />, document.querySelector('#filtered_search'));
    });
}

class Offers extends React.Component {
    render() {
        const offers = this.props.data.offers;
        const offeritems = offers.map((offer) =>
        <div key={offer.id}>
            <div className="card mb-2 rounded-6 shadow p-2" style={{ minHeight: '300px', marginTop: '0px', minWidth: '300px' }}>
                <div className="card-body">
                    <div className="row">
                        <div className='col' style={{ textAlign: 'left', color: '#2798F8', minWidth: '250px', marginBottom: '20px' }}>
                            <h4>{offer.name}</h4>
                            <h5>Total price for {offer.time_delta} day(s): {offer.total_price} USD</h5>
                            <div className="lh-sm">{offer.description}</div>
                            <div className="align-bottom" style={{ color: 'grey', fontSize: '15px' }}>Created in {offer.timestamp}</div>
                        </div>
                        <div className='col' style={{ textAlign: 'right' }}>
                            <img src={offer.photo} alt="image" className="rounded float-start " style={{ width: '250px' }} />
                        </div>
                    </div>
                </div>
                <div className="row align-bottom" style={{ textAlign: 'left', margin: '10px'}}>
                    <div className="col" style={{ color: '#2798F8' }}><img src='static/transport/icons/icon_location.svg' style={{ width: '14px', verticalAlign: '-15%', marginRight: '5px'}} />{offer.pick_up_location}</div> 
                    <div className="col" style={{ textAlign: 'right' }}><button type="button" className="btn btn-warning" style={{ width: '125px', color: 'white' }}><b>RENT</b></button></div>
                </div>
            </div>
        </div>

        );
        return (
            <div>{offeritems}</div>
        );
    }
}
