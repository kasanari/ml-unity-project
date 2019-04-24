using System.Collections.Generic;
using UnityEngine;
using MLAgents;

public class RollerAgent : Agent
{
    Rigidbody rBody;
    void Start()
    {
        rBody = GetComponent<Rigidbody>();
    }

    //private Transform target;
    private RollerAcademy academy;

    public override void InitializeAgent()
    {
        academy = FindObjectOfType(typeof(RollerAcademy)) as RollerAcademy;

    }

    public override void AgentReset()
    {
        print("Reset");
        /*if (this.transform.position.y < 0)
        {
            // If the Agent fell, zero its momentum
            this.rBody.angularVelocity = Vector3.zero;
            this.rBody.velocity = Vector3.zero;
            this.transform.position = new Vector3(0, 0.5f, 0);
        }*/
        academy.AcademyReset();

    }

    public override void CollectObservations()
    {
        // Target and Agent positions
        AddVectorObs(academy.Target.position);
        AddVectorObs(this.transform.position);

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
        float distanceToTarget = Vector3.Distance(this.transform.position,
                                                  academy.Target.position);

        // Reached target
        if (distanceToTarget < 1.5f)
        {
            SetReward(1000.0f);
            Done();
        } else
        {
            SetReward(-0.1f);
        }

        // Fell off platform
        if (this.transform.position.y < 0)
        {
            SetReward(-100.0f);
            Done();
        }

    }
}