import React from 'react'
import { Card, CardContent, Typography, Grid } from '@material-ui/core';
import CountUp from 'react-countup';
import cx from 'classnames';

import styles from './index.module.css';
interface item {
    value?: number;
    detail?: string;
}
interface ICardsItemPops {
    confirmed: item;
    recovered: item;
    deaths: item;
    lastUpdate: string;
}


const Cards :React.FC<ICardsItemPops>= ({confirmed, recovered, deaths,lastUpdate })  => {

   
    if(!confirmed ) {
        return   <div>  Loading........ </div> 
    }else {
        return (
            <div className={styles.container}>
            <Grid container spacing={3} justify="center">
                <Grid item xs={12} md={3} component={Card} className={cx(styles.card, styles.infected)}>
                <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                    Infected
                    </Typography>
                    <Typography variant="h5" component="h2">
                    <CountUp start={0} end={confirmed.value || 0} duration={2.75} separator="," />
                    </Typography>
                    <Typography color="textSecondary">
                    {new Date(lastUpdate).toDateString()}
                    </Typography>
                    <Typography variant="body2" component="p">
                        COVID-19 Infected.
                    </Typography>
                </CardContent>
                </Grid>
                <Grid item xs={12} md={3} component={Card} className={cx(styles.card, styles.recovered)}>
                <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                    Recovered
                    </Typography>
                    <Typography variant="h5" component="h2">
                    <CountUp start={0} end={ recovered.value || 0} duration={2.75} separator="," />
                    </Typography>
                    <Typography color="textSecondary">
                    {new Date(lastUpdate).toDateString()}
                    </Typography>
                    <Typography variant="body2" component="p">
                        COVID-19 Recovered.
                    </Typography>
                </CardContent>
                </Grid>
                <Grid item xs={12} md={3} component={Card} className={cx(styles.card, styles.deaths)}>
                <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                    Deaths
                    </Typography>
                    <Typography variant="h5" component="h2">
                    <CountUp start={0} end={deaths.value || 0} duration={2.75} separator="," />
                    </Typography>
                    <Typography color="textSecondary">
                    {new Date(lastUpdate).toDateString()}
                    </Typography>
                    <Typography variant="body2" component="p">
                        COVID-19 Deaths.
                    </Typography>
                </CardContent>
                </Grid>
            </Grid>
            </div>
        );
    }
}


export default Cards ;