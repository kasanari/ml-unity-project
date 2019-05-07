﻿using System.Collections.Generic;
using UnityEngine;
using MLAgents;

public class RollerAgent : Agent
{
    Rigidbody rBody;
    void Start()
    {
        rBody = GetComponent<Rigidbody>();
    }

    public Transform target;
    private RollerAcademy academy;

    public void SetSpawnPositions()
    {
        Random random = new Random();
        Vector3 start_point = new Vector3(-17.5f, 0.5f, -17.5f);

        target.localPosition = start_point + (new Vector3(Random.Range(0, 7) * 5, 0, Random.Range(0, 7) * 5));
        print("Set goal at: " + target.localPosition);
        this.transform.localPosition = start_point + (new Vector3(Random.Range(0, 7) * 5, 0, Random.Range(0, 7) * 5));
        this.rBody.velocity = Vector3.zero;
        this.rBody.angularVelocity = Vector3.zero;
        print("Set agent at: " + target.localPosition);
    }

    public override void InitializeAgent()
    {
        academy = FindObjectOfType(typeof(RollerAcademy)) as RollerAcademy;

    }

    public override void AgentReset()
    {
        print("Reset");

        SetSpawnPositions();
    }

    public override void CollectObservations()
    {
        // Target and Agent positions
        AddVectorObs(target.localPosition);
        AddVectorObs(this.transform.localPosition);

        // Agent velocity
        AddVectorObs(rBody.velocity.x);
        AddVectorObs(rBody.velocity.z);
    }

    public float speed = 10;
    public override void AgentAction(float[] vectorAction, string textAction)
    {
        // Actions, size = 2
        Vector3 controlSignal = Vector3.zero;
        controlSignal.x = vectorAction[0];
        controlSignal.z = vectorAction[1];
        rBody.AddForce(controlSignal * speed);

        // Rewards
        float distanceToTarget = Vector3.Distance(this.transform.localPosition,
                                                  target.localPosition);

        // Reached target
        if (distanceToTarget < 1.5f)
        {
            SetReward(100.0f);
            Done();
        } else
        {
            SetReward(-0.1f);
        }

        // Fell off platform
        if (this.transform.localPosition.y < 0)
        {
            Done();
        }
        
    }
}