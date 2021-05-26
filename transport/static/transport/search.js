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

    // Place by order
    $('#order').change(event => {
        $('#new_search').hide();
        load(event.target.value);
    })
)

function load(sort_value) {

    // Get new posts and add posts
    fetch(`/filter?filters=${filters}&order=${sort_value}`)
    .then(response => response.json())
    .then(data => {
        $('#min_price').text(data.min_price);
        $('#max_price').text(data.max_price);
        ReactDOM.render(<Offers data={data} />, document.querySelector('#filtered_search'));
    });
}

class Offers extends React.Component {
    render() {
        const offers = this.props.data.offers;
        const offeritems = offers.map((offer) =>

            <div  key={offer.id}>
                <div className="card mb-2 rounded-6 shadow p-2" style={{ minHeight: '300px', minWidth: '300px', maxWidth: '1000px', borderRadius: '15px' }}>
                    <div className="card-body" style={{ padding: '15px' }}>
                        <div className="row">
                            <div className='col' style={{ textAlign: 'left', minWidth: '270px', maxWidth: '340px' }}>
                                <img src={offer.photo} alt="image"  style={{ maxWidth: '100%', minWidth: 'none', borderRadius: '10px' }} />
                            </div>
                            <div className='col' style={{ textAlign: 'left', minWidth: '250px', marginTop: '5px', marginBottom: '0px', borderRight: '1px solid #2a9d8f' }}>
                                <h4 style={{ color: '#2a9d8f' }}>{offer.name}</h4>
                                <br />
                                <div name="icons_gread" style={{ maxWidth: '200px' }}>
                                    <div className="row">
                                        <div className="col" style={{ marginTop: '7px' }}><img src='/static/transport/icons/icon_man.svg' style={{ width: '17px', verticalAlign: '-10%', marginRight: '5px'}} />{offer.passenger_places}</div>
                                        <div className="col" style={{ marginTop: '7px' }}><img src='/static/transport/icons/icon_conditioner.svg' style={{ width: '17px', verticalAlign: '-15%', marginRight: '5px', }} />A/C {offer.air_conditioner}</div>
                                    </div>
                                    <div className="row">
                                        <div className="col" style={{ marginTop: '7px' }}><img src='/static/transport/icons/icon_bagage.svg' style={{ width: '17px', verticalAlign: '-10%', marginRight: '5px'}} />{offer.baggage_places}</div>
                                        <div className="col" style={{ marginTop: '7px' }}><img src='/static/transport/icons/icon_gearbox.svg' style={{ width: '17px', verticalAlign: '-10%', marginRight: '5px'}} />{offer.automat_gearbox}</div>
                                    </div>
                                </div>
                                <br /><br />
                                <div style={{ textAlign: 'left', height: '100%', marginTop: 'auto'}}>
                                    <div className='row'>
                                        <div className="col" style={{ marginTop: '7px' }}><img src='/static/transport/icons/user.png' style={{ width: '25px', verticalAlign: '-40%', marginRight: '5px' }} /><a href={offer.owner_page} className="btn btn-link" style={{color: 'black', padding: '0%', fontWeight: '800'}}>{offer.owner}</a></div>
                                        <div className="col" style={{ marginTop: '7px', fontSize: '17px' }}><img src='/static/transport/icons/icon_star.svg' style={{ width: '18px', verticalAlign: '-11%', marginRight: '5px' }} />{offer.owner_rating}/<span style={{ fontSize: '11.5px' }}>5</span> <a href={offer.owner_page} className="btn btn-link" style={{ fontSize: '15px', color: 'black', padding: '0%', paddingBottom: '3px', textDecoration: 'underline' }}>{offer.responses_count} reviews</a></div>
                                    </div>
                                    <div className='row'>
                                        <div className="col" style={{ marginTop: '7px', paddingLeft: '20px' }}><img src='/static/transport/icons/icon_location.svg' style={{ width: '14px', verticalAlign: '-15%', marginRight: '5px' }} />{offer.pick_up_location}</div>
                                        <div className="col" style={{ marginTop: '7px' }}></div>
                                    </div>
                                    
                                </div>
                            </div>
                            <div className="col" style={{ marginTop: 'auto', textAlign: 'left', maxWidth: '200px' }}>
                                <div style={{ marginBottom: '10px', fontSize: '18px' }}>
                                    Total:
                                    <h4 style={{ marginBottom: '0%', color: '#2a9d8f' }}><b>${offer.total_price}</b></h4>
                                    for {offer.time_delta} day(s)
                                </div>
                                <div className="row align-bottom" style={{ textAlign: 'left' }}>
                                    <div className="col" style={{ marginBottom: '10px' }}><img src='/static/transport/icons/check.png' style={{ width: '20px', verticalAlign: '-10%', marginRight: '5px' }} />Free canelation</div> 
                                </div>
                                <a href={offer.details} ><button type="button" className="btn btn-warning" style={{ width: '100%', color: 'white' }}><b>DETAILS</b></button></a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>   

        );
        return (
            <div>{offeritems}</div>
        );
    }
}
